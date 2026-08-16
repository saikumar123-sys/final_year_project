from flask import render_template, redirect, url_for, flash, request, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from extensions import db
from models import User, Emission, MarketOrder, MarketConfig, Baseline, CreditRetirement, EmissionDocument
from werkzeug.utils import secure_filename
import uuid

from werkzeug.security import generate_password_hash, check_password_hash
import web3_utils # Import the new module
from sqlalchemy import func
import os

# --- Auth Routes ---
def calculate_market_price():

    config = MarketConfig.query.first()

    base_price = config.base_price if config else 500
    adjustment_factor = config.adjustment_factor if config else 0.5

    # Total credits available (supply)
    supply = db.session.query(func.sum(Emission.credits_earned)).scalar() or 0

    # Total penalties required (demand)
    demand = db.session.query(func.sum(Emission.penalty)).scalar() or 0

    # demand-supply ratio model
    ratio = (demand - supply) / (supply + demand + 1)

    market_price = base_price * (1 + adjustment_factor * ratio)

    # Stability controls (real carbon exchanges use this)
    min_price = base_price * 0.3
    max_price = base_price * 3

    market_price = max(min_price, min(market_price, max_price))

    return round(market_price, 2)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        
        # Generate Wallet
        wallet_address, private_key = web3_utils.create_wallet()

        # we don't store private key for Ganache managed accounts
        # private_key = "GANACHE"

        
        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            role=role,
            wallet_address=wallet_address,
            private_key=private_key,
            is_approved=False,     # important
            is_suspended=False
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration request sent! Wait for admin approval.", "info")
        return redirect(url_for('login'))

        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):

            # ADMIN LOGIN
            if user.role == 'admin':
                login_user(user)
                return redirect(url_for('dashboard'))

            # INDUSTRY NOT APPROVED
            if not user.is_approved:
                flash("Your account is pending admin approval.", "warning")
                return redirect(url_for('login'))

            # SUSPENDED ACCOUNT
            if user.is_suspended:
                flash("Your account has been suspended by admin.", "danger")
                return redirect(url_for('login'))

            # APPROVED INDUSTRY
            login_user(user)
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid email or password", "danger")

        # else:
        #     flash('Login Failed')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

from sqlalchemy import func

from sqlalchemy import func

from sqlalchemy import func
@app.route('/dashboard')
@login_required
def dashboard():

    # ======================================================
    # GLOBAL MARKET ECONOMICS (Used by BOTH Admin & Industry)
    # ======================================================

    # Total penalties = demand
    total_penalties = db.session.query(func.sum(Emission.penalty)).scalar() or 0

    # Calculate REAL supply (tradable credits)
    all_industries = User.query.filter_by(role='industry').all()

    supply = 0

    for industry in all_industries:
        try:
            # Fetch REAL balance from blockchain
            balance = web3_utils.get_token_balance(industry.wallet_address)
            industry.blockchain_balance = float(balance) # Attach to object for template
            supply += industry.blockchain_balance
        except Exception as e:
            print(f"Error fetching balance for {industry.username}: {e}")
            industry.blockchain_balance = 0.0

    # demand = total penalties
    demand = total_penalties

    # market price (your formula)
    market_price = calculate_market_price()

    # ======================================================
    # ================= ADMIN DASHBOARD ====================
    # ======================================================
    if current_user.role == 'admin':

        total_industries = len(all_industries)

        total_credits = db.session.query(func.sum(Emission.credits_earned)).scalar() or 0
        total_trades = MarketOrder.query.filter_by(status='Completed').count()

        # industries = User.query.filter_by(role='industry').all() # removed redundant query

        penalty_industries = Emission.query.filter(
            Emission.penalty > 0
        ).distinct(Emission.industry_id).count()

        return render_template(
            'admin_dashboard.html',
            total_industries=total_industries,
            total_credits=total_credits,
            total_penalties=total_penalties,
            total_trades=total_trades,
            industries=all_industries, # Passed with balances attached
            supply=supply,
            demand=demand,
            market_price=market_price,
            penalty_industries=penalty_industries
        )

    # ======================================================
    # ================= INDUSTRY SECURITY ==================
    # ======================================================

    if not current_user.is_approved:
        logout_user()
        flash("Your account is waiting for admin approval.", "warning")
        return redirect(url_for('login'))

    if current_user.is_suspended:
        logout_user()
        flash("Your account has been suspended by admin.", "danger")
        return redirect(url_for('login'))

    # ======================================================
    # ================= INDUSTRY DASHBOARD =================
    # ======================================================

    username = current_user.username

    # Total earned credits
    total_credits = db.session.query(func.sum(Emission.credits_earned))\
        .filter_by(industry_id=current_user.id).scalar() or 0

    # Total penalty
    total_penalty = db.session.query(func.sum(Emission.penalty))\
        .filter_by(industry_id=current_user.id).scalar() or 0

    # Credits sold
    sold_credits = db.session.query(func.sum(MarketOrder.amount))\
        .filter_by(seller_id=current_user.id, status="Completed").scalar() or 0

    # Credits bought
    bought_credits = db.session.query(func.sum(MarketOrder.amount))\
        .filter_by(buyer_id=current_user.id, status="Completed").scalar() or 0

    # Available credits (REAL BLOCKCHAIN BALANCE)
    try:
        blockchain_balance = web3_utils.get_token_balance(current_user.wallet_address)
        # Convert Decimal/float to float just in case
        available_credits = float(blockchain_balance)
    except Exception as e:
        print(f"Error fetching balance: {e}")
        available_credits = 0.0

    # --- AUTO-DEDUCT PENALTY LOGIC ---
    if total_penalty > 0 and available_credits >= total_penalty:
        try:
            # 0. Ensure ETH for gas
            funding_success = web3_utils.check_and_fund_wallet(current_user.wallet_address)
            if not funding_success:
                print("Auto-deduction skipped: Could not fund wallet for gas")
            else:
                # 1. Burn tokens
                tx_hash = web3_utils.burn_tokens(current_user.private_key, total_penalty)
                
                # 2. Update DB
                emissions = Emission.query.filter_by(industry_id=current_user.id).all()
                for e in emissions:
                    e.penalty = 0
                    e.status = "Approved"
                db.session.commit()
                
                # 3. Update local variables for display
                available_credits -= total_penalty
                total_penalty = 0.0
                
                flash(f"Automatic Action: Penalty offset using available credits. Tx: {tx_hash}", "success")
            
        except Exception as e:
            print(f"Auto-deduction failed: {e}")
            # Don't flash every time if it's a gas error, just log it. 
            # User will see 'Pay Penalty' button anyway.

    # Transaction count
    transactions = MarketOrder.query.filter(
        (MarketOrder.seller_id == current_user.id) |
        (MarketOrder.buyer_id == current_user.id),
        MarketOrder.status == "Completed"
    ).count()

    return render_template(
        'industry_dashboard.html',
        username=username,
        my_credits=total_credits,
        my_penalty=total_penalty,
        available_credits=available_credits,
        transactions=transactions,
        supply=supply,
        demand=demand,
        market_price=market_price
    )




# --- Industry Routes ---
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xlsx', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/report_emission', methods=['GET', 'POST'])
@login_required
def report_emission():

    if request.method == 'POST':
        # Collect form data
        form_data = {
            'year': request.form.get('year', ''),
            'sector': request.form.get('sector', 'Manufacturing'),
            'gas_type': request.form.get('gas_type', 'CO2'),
            'reported': request.form.get('reported', '')
        }

        # ---- Track emission context for uploads ----
        current_context = f"{form_data['year']}|{form_data['sector']}|{form_data['gas_type']}"

        # ---- If emission context changed, clear previous documents ----
        previous_context = session.get('doc_context')
        existing_docs = EmissionDocument.query.filter_by(industry_id=current_user.id).all()
        should_clear = False

        if previous_context and previous_context != current_context:
            # Context explicitly changed (year/sector/gas_type differ)
            should_clear = True
        elif not previous_context and len(existing_docs) > 0:
            # No context in session but stale documents exist (e.g. from a previous submission)
            should_clear = True

        if should_clear and len(existing_docs) > 0:
            for doc in existing_docs:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(doc)
            db.session.commit()
            session.pop('doc_context', None)
            flash("New emission entry — previous documents cleared. Please upload new documents.", "info")

        # ---- Handle file upload if a file was attached ----
        uploaded_file = request.files.get('document')
        if uploaded_file and uploaded_file.filename and uploaded_file.filename != '':
            existing_count = EmissionDocument.query.filter_by(industry_id=current_user.id, status='PENDING VERIFICATION').count()
            if existing_count >= 2:
                flash("You have already uploaded 2 documents.", "warning")
            elif allowed_file(uploaded_file.filename):
                original_name = secure_filename(uploaded_file.filename)
                unique_name = f"{uuid.uuid4().hex}_{original_name}"
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))

                doc = EmissionDocument(
                    industry_id=current_user.id,
                    filename=unique_name,
                    original_name=original_name,
                    status='PENDING VERIFICATION'
                )
                db.session.add(doc)
                db.session.commit()

                session['doc_context'] = current_context
                flash("Document uploaded successfully!", "success")
            else:
                flash(f"File '{uploaded_file.filename}' has an unsupported format.", "warning")

        # ---- Refresh documents after potential upload ----
        my_documents = EmissionDocument.query.filter_by(
            industry_id=current_user.id
        ).order_by(EmissionDocument.uploaded_at.desc()).all()

        has_documents = len(my_documents) > 0
        docs_approved = has_documents and all(d.status == 'APPROVED' for d in my_documents)

        # ---- If documents are not approved, save form data and redirect ----
        if not docs_approved:
            docs_pending = has_documents and any(d.status == 'PENDING VERIFICATION' for d in my_documents)
            docs_rejected = has_documents and all(d.status == 'REJECTED' for d in my_documents)

            if has_documents and docs_pending:
                flash("Your documents are pending admin verification.", "info")
            elif has_documents and docs_rejected:
                flash("Your documents have been rejected. Please contact the admin.", "danger")

            # Save form data to session so it survives the redirect
            session['emission_form_data'] = form_data
            if not session.get('doc_context'):
                session['doc_context'] = current_context
            return redirect(url_for('report_emission'))

        # ---- Documents are approved → process the emission report ----
        year = int(form_data['year'])
        sector = form_data['sector']
        gas_type = form_data['gas_type']
        reported = float(form_data['reported'])

        existing_report = Emission.query.filter_by(
            industry_id=current_user.id,
            year=year,
            sector=sector,
            gas_type=gas_type
        ).first()

        if existing_report:
            flash(f"Emission report for {year} ({gas_type}) already exists.", "warning")
            session['emission_form_data'] = form_data
            return redirect(url_for('report_emission'))

        baseline_obj = Baseline.query.filter_by(
            sector=sector,
            gas_type=gas_type,
            year=year
        ).first()

        if not baseline_obj:
            flash("Baseline not set by admin yet", "danger")
            session['emission_form_data'] = form_data
            return redirect(url_for('report_emission'))

        baseline = baseline_obj.allowed_emission

        emission = Emission(
            industry_id=current_user.id,
            year=year,
            sector=sector,
            gas_type=gas_type,
            reported_amount=reported,
            baseline_amount=baseline
        )

        if reported < baseline:
            credits = baseline - reported
            emission.credits_earned = credits
            emission.status = "Approved"
            tx_hash = web3_utils.mint_tokens(current_user.wallet_address, credits)
            emission.blockchain_tx = tx_hash
            flash(f"{credits} credits minted. TX: {tx_hash}", "success")
        else:
            penalty = reported - baseline
            emission.penalty = penalty
            emission.status = "Penalty"
            flash(f"Penalty: {penalty} credits required", "warning")

        db.session.add(emission)
        db.session.commit()

        # Clear session and documents — fresh start after successful submission
        submitted_docs = EmissionDocument.query.filter_by(industry_id=current_user.id).all()
        for doc in submitted_docs:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(doc)
        db.session.commit()
        session.pop('doc_context', None)
        session.pop('emission_form_data', None)

        return redirect(url_for('report_emission'))

    # ---------- GET REQUEST ----------
    # Read form data from session WITHOUT removing it — it persists across refreshes
    # Only cleared after successful report submission (see POST handler above)
    form_data = session.get('emission_form_data', {
        'year': '',
        'sector': 'Manufacturing',
        'gas_type': 'CO2',
        'reported': ''
    })

    my_documents = EmissionDocument.query.filter_by(
        industry_id=current_user.id
    ).order_by(EmissionDocument.uploaded_at.desc()).all()

    has_documents = len(my_documents) > 0
    docs_approved = has_documents and all(d.status == 'APPROVED' for d in my_documents)
    docs_pending = has_documents and any(d.status == 'PENDING VERIFICATION' for d in my_documents)
    docs_rejected = has_documents and all(d.status == 'REJECTED' for d in my_documents)

    response = make_response(render_template('report_emission.html',
                           documents=my_documents,
                           docs_approved=docs_approved,
                           has_documents=has_documents,
                           docs_pending=docs_pending,
                           docs_rejected=docs_rejected,
                           form_data=form_data))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# --- Market Routes ---
@app.route('/market')
@login_required
def market():
    all_orders = MarketOrder.query.filter_by(status='Open').all()
    valid_orders = []

    for order in all_orders:
        try:
            seller = User.query.get(order.seller_id)
            if not seller or not seller.wallet_address:
                continue
                
            balance = float(web3_utils.get_token_balance(seller.wallet_address))
            
            # Attach balance to order object for template logic
            order.seller_balance = balance
            
            # Filter out own orders here (Fixes template "else" block bug)
            if order.seller_id != current_user.id:
                valid_orders.append(order)
                
        except Exception as e:
            print(f"Error validating order {order.id}: {e}")
            # If blockchain error, treat as 0 balance but still show
            order.seller_balance = 0
            if order.seller_id != current_user.id:
                valid_orders.append(order)

    market_price = calculate_market_price()
    
    # --- FEATURE: Show industries with credits (Potential Sellers) ---
    all_industries = User.query.filter_by(role='industry').all()
    sellers_with_credits = []
    
    for industry in all_industries:
        if industry.id == current_user.id:
            continue # Skip self within potential sellers list too? (Optional, but cleaner)
            
        try:
            bal = float(web3_utils.get_token_balance(industry.wallet_address))
            if bal > 0:
                industry.blockchain_balance = bal
                sellers_with_credits.append(industry)
        except Exception as e:
            print(f"Error fetching balance for potential seller {industry.username}: {e}")

    available_credits = 0.0
    if current_user.is_authenticated and current_user.role == 'industry':
        try:
            available_credits = float(web3_utils.get_token_balance(current_user.wallet_address))
        except:
            available_credits = 0.0

    return render_template('market.html', orders=valid_orders, market_price=market_price, available_credits=available_credits, sellers_with_credits=sellers_with_credits)

@app.route('/market/sell', methods=['GET', 'POST'])
@login_required
def create_listing():

    if request.method == 'POST':

        try:
            amount = float(request.form.get('amount'))

            if amount <= 0:
                flash("Invalid credit amount", "danger")
                return redirect(url_for('market'))

            # 1️⃣ Penalty check FIRST
            total_penalty = db.session.query(func.sum(Emission.penalty))\
                .filter_by(industry_id=current_user.id).scalar() or 0

            if total_penalty > 0:
                flash("You must offset your emission penalty before trading", "danger")
                return redirect(url_for('dashboard'))

            # 2️⃣ Check blockchain balance (REAL balance)
            balance = web3_utils.get_token_balance(current_user.wallet_address)

            if balance < amount:
                flash("You do not have enough blockchain credits to sell", "danger")
                return redirect(url_for('market'))

            # 3️⃣ Approve exchange (CRITICAL STEP)
            # platform admin will execute transferFrom, so seller must approve admin
            approval_tx = web3_utils.approve_tokens(current_user.private_key, amount)

            # verify approval mined
            receipt = web3_utils.wait_for_receipt(approval_tx)

            if receipt.status != 1:
                flash("Blockchain approval failed. Try again.", "danger")
                return redirect(url_for('market'))

            # 4️⃣ Get dynamic market price
            price = calculate_market_price()

            # 5️⃣ Create order ONLY AFTER SUCCESSFUL APPROVAL
            order = MarketOrder(
                seller_id=current_user.id,
                amount=amount,
                price_per_credit=price,
                status="Open",
                approval_status="None"
            )

            db.session.add(order)
            db.session.commit()

            flash(f"Sell order created successfully at ₹{price} per CCT", "success")
            return redirect(url_for('market'))

        except Exception as e:
            flash(f"Listing failed: {str(e)}", "danger")
            return redirect(url_for('market'))

    return render_template('create_listing.html')



@app.route('/market/buy/<int:order_id>')
@login_required
def buy_credit(order_id):

    order = MarketOrder.query.get_or_404(order_id)

    # Cannot buy own listing
    if order.seller_id == current_user.id:
        flash("You cannot buy your own credits", "warning")
        return redirect(url_for('market'))

    # Cannot request again
    if order.approval_status == "Pending":
        flash("Request already sent", "warning")
        return redirect(url_for('market'))

    # Cannot buy completed order
    if order.status == "Completed":
        flash("Credits already sold", "danger")
        return redirect(url_for('market'))

    # Send request to seller
    order.buyer_id = current_user.id
    order.approval_status = "Pending"

    db.session.commit()

    flash("Purchase request sent to seller for approval", "info")
    return redirect(url_for('market'))

# --- Admin Routes ---
@app.route('/admin/deploy')
@login_required
def deploy_contract_route():

    if current_user.role != 'admin':
        return "Unauthorized Access"

    try:
        address, abi = web3_utils.deploy_contract()

        return f"""
        <h2>Contract Successfully Deployed!</h2>
        <p><b>Contract Address:</b> {address}</p>
        <p>Copy this address and paste into your .env file as CONTRACT_ADDRESS</p>
        """

    except Exception as e:
        return f"<h2>Deployment Error</h2><pre>{str(e)}</pre>"

@app.route('/offset/<int:emission_id>')
@login_required
def offset_emission(emission_id):

    emission = Emission.query.get_or_404(emission_id)

    if emission.penalty <= 0:
        flash("No penalty to offset", "warning")
        return redirect(url_for('dashboard'))

    try:
        # FIXED: Get real private key
        industry_private_key = web3_utils.get_ganache_private_key(current_user.wallet_address)
        
        if industry_private_key:
            tx_hash = web3_utils.burn_tokens(industry_private_key, emission.penalty)
        else:
            flash("Blockchain Error: Private key not found", "danger")
            return redirect(url_for('dashboard'))

        retirement = CreditRetirement(
            industry_id=current_user.id,
            credits_retired=emission.penalty,
            tx_hash=tx_hash
        )

        db.session.add(retirement)
        db.session.commit()

        flash(f"Emission offset successful! TX: {tx_hash}", "success")

    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for('dashboard'))
@app.route('/admin/baseline', methods=['GET','POST'])
@login_required
def set_baseline():

    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        sector = request.form.get('sector')
        gas_type = request.form.get('gas_type')
        year = int(request.form.get('year'))
        allowed = float(request.form.get('allowed'))

        baseline = Baseline(
            sector=sector,
            gas_type=gas_type,
            year=year,
            allowed_emission=allowed
        )

        db.session.add(baseline)
        db.session.commit()

        flash("Baseline emission set successfully", "success")
        return redirect(url_for('dashboard'))

    baselines = Baseline.query.all()
    return render_template('set_baseline.html', baselines=baselines)

@app.route('/admin/market_config', methods=['GET','POST'])
@login_required
def market_config():

    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))

    config = MarketConfig.query.first()

    if request.method == 'POST':
        base_price = float(request.form.get('base_price'))
        adjustment_factor = float(request.form.get('adjustment_factor'))

        if not config:
            config = MarketConfig()

        config.base_price = base_price
        config.adjustment_factor = adjustment_factor

        db.session.add(config)
        db.session.commit()

        flash("Market regulation updated successfully", "success")
        return redirect(url_for('dashboard'))

    return render_template('market_config.html', config=config)

@app.route('/admin/industries')
@login_required
def manage_industries():

    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industries = User.query.filter_by(role='industry').all()

    # Create list of dicts or attach to objects to display balance
    for industry in industries:
        try:
            balance = web3_utils.get_token_balance(industry.wallet_address)
            industry.blockchain_balance = float(balance)
        except:
            industry.blockchain_balance = 0.0

    return render_template('manage_industries.html', industries=industries)
@app.route('/admin/approve/<int:industry_id>')
@login_required
def approve_industry(industry_id):

    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industry = User.query.get_or_404(industry_id)
    industry.is_approved = True

    db.session.commit()
    flash(f"{industry.username} approved successfully", "success")

    return redirect(url_for('manage_industries'))
@app.route('/admin/reject/<int:industry_id>')
@login_required
def reject_industry(industry_id):

    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industry = User.query.get_or_404(industry_id)

    db.session.delete(industry)
    db.session.commit()

    flash("Industry registration rejected", "warning")
    return redirect(url_for('manage_industries'))
@app.route('/admin/suspend/<int:industry_id>')
@login_required
def suspend_industry(industry_id):

    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industry = User.query.get_or_404(industry_id)

    industry.is_suspended = not industry.is_suspended

    db.session.commit()

    flash("Industry suspension status updated", "info")
    return redirect(url_for('manage_industries'))
@app.route('/admin/emissions/<int:industry_id>')
@login_required
def view_emissions(industry_id):


    records = Emission.query.filter_by(industry_id=industry_id).all()

    total_emission = sum(e.reported_amount for e in records)
    avg_reduction = sum((e.baseline_amount - e.reported_amount) for e in records if e.baseline_amount > e.reported_amount)

    data_points = len(records)

    return render_template(
        'industry_emissions_analytics.html',
        records=records,
        total_emission=total_emission,
        avg_reduction=avg_reduction,
        data_points=data_points
    )
@app.route('/market/request/<int:order_id>')
@login_required
def request_buy(order_id):

    order = MarketOrder.query.get_or_404(order_id)
    
    # Update price to current market price (Dynamic Pricing)
    current_market_price = calculate_market_price()
    order.price_per_credit = current_market_price

    order.buyer_id = current_user.id
    order.approval_status = 'Pending'

    db.session.commit()

    flash("Purchase request sent to seller", "info")
    return redirect(url_for('market'))

@app.route('/market/direct_buy', methods=['POST'])
@login_required
def request_direct_buy():
    try:
        seller_id = int(request.form.get('seller_id'))
        amount = float(request.form.get('amount'))
        
        if seller_id == current_user.id:
            flash("You cannot buy from yourself.", "warning")
            return redirect(url_for('market'))
            
        if amount <= 0:
            flash("Invalid amount.", "danger")
            return redirect(url_for('market'))

        seller = User.query.get_or_404(seller_id)
        
        # Check seller balance locally first (Real check happens on approval)
        seller_balance = float(web3_utils.get_token_balance(seller.wallet_address))
        if seller_balance < amount:
             flash(f"Seller only has {seller_balance} CCT available.", "warning")
             return redirect(url_for('market'))
             
        # Calculate price
        market_price = calculate_market_price()
        
        # Create Order
        order = MarketOrder(
            seller_id=seller_id,
            buyer_id=current_user.id,
            amount=amount,
            price_per_credit=market_price,
            status="Open", # Or 'Pending Approval' logic
            approval_status="Pending"
        )
        
        db.session.add(order)
        db.session.commit()
        
        flash(f"Buy request for {amount} CCT sent to {seller.username}", "success")
        
    except Exception as e:
        flash(f"Request failed: {str(e)}", "danger")
        
    return redirect(url_for('market'))
@app.route('/market/approve/<int:order_id>', methods=['POST'])
@login_required
def approve_trade(order_id):

    order = MarketOrder.query.get_or_404(order_id)

    # Only seller can approve
    if order.seller_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect(url_for('dashboard'))

    # Must be pending request
    if order.approval_status != "Pending" or order.status == "Completed":
        flash("This request is no longer valid", "warning")
        return redirect(url_for('sell_requests'))

    seller = User.query.get(order.seller_id)
    buyer = User.query.get(order.buyer_id)

    try:
        # Convert to wei
        amount_wei = web3_utils.web3.to_wei(order.amount, 'ether')

        # 1️⃣ Check seller balance on blockchain
        seller_balance = web3_utils.get_token_balance(seller.wallet_address)

        if seller_balance < order.amount:
            flash("Seller does not have enough blockchain credits", "danger")
            return redirect(url_for('sell_requests'))

        # 2️⃣ Check allowance & AUTO-APPROVE for Direct Trades
        admin_address = web3_utils.get_admin_address()
        allowance = web3_utils.get_allowance(seller.wallet_address, admin_address)
        allowance_wei = web3_utils.web3.to_wei(allowance, 'ether')

        if allowance_wei < amount_wei:
            # If allowance is low, check if we can auto-approve (Demo Feature)
            # In a real app, seller would sign a tx here.
            if seller.private_key:
                 print(f"Auto-approving for Direct Buy: {seller.username}")
                 approve_tx = web3_utils.approve_tokens(seller.private_key, order.amount)
                 # Re-check allowance just in case
            else:
                 flash("Seller has not approved credits and private key missing.", "warning")
                 return redirect(url_for('sell_requests'))

        # 3️⃣ EXECUTE BLOCKCHAIN TRANSFER (credits go from seller → buyer)
        tx_hash = web3_utils.transfer_tokens(
            seller.wallet_address,
            buyer.wallet_address,
            order.amount
        )

        # 4️⃣ MINT SELLER REWARD: seller gets (sold_credits × market_price) as new credits
        seller_reward = order.amount * order.price_per_credit
        reward_tx = web3_utils.mint_tokens(seller.wallet_address, seller_reward)

        # ---------------- DB UPDATE ONLY AFTER SUCCESS ----------------
        order.status = "Completed"
        order.approval_status = "Approved"
        order.tx_hash = tx_hash

        db.session.commit()

        flash(f"Trade successful! You sold {order.amount} CCT and received {seller_reward} CCT as reward (₹{order.price_per_credit}/credit). Tx: {tx_hash}", "success")

    except Exception as e:
        order.status = "Failed"
        db.session.commit()

        flash(f"Trade failed: {str(e)}", "danger")

    return redirect(url_for('sell_requests'))


@app.route('/market/reject/<int:order_id>', methods=['POST'])
@login_required
def reject_trade(order_id):

    order = MarketOrder.query.get_or_404(order_id)

    # only seller can reject
    if order.seller_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect(url_for('dashboard'))

    # reject order but keep buyer_id for audit trail
    order.approval_status = "Rejected"
    order.status = "Rejected"

    db.session.commit()

    flash("Trade request rejected successfully", "warning")
    return redirect(url_for('sell_requests'))

@app.route('/industry/emissions')
@login_required
def emission_analytics():

    records = Emission.query.filter_by(industry_id=current_user.id).all()

    total_emission = sum(e.reported_amount for e in records)
    avg_reduction = sum((e.baseline_amount - e.reported_amount) for e in records if e.baseline_amount > e.reported_amount)

    data_points = len(records)

    return render_template(
        'industry_emissions_analytics.html',
        records=records,
        total_emission=total_emission,
        avg_reduction=avg_reduction,
        data_points=data_points
    )
@app.route('/sell_requests')
@login_required
def sell_requests():

    if current_user.role != 'industry':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    requests = MarketOrder.query.filter_by(
        seller_id=current_user.id,
        approval_status='Pending'
    ).all()

    market_price = calculate_market_price()

    return render_template('sell_requests.html', requests=requests, market_price=market_price)
@app.route('/offset_penalty')
@login_required
def offset_penalty():
    # 1. Get Total Penalty
    total_penalty = db.session.query(func.sum(Emission.penalty))\
        .filter_by(industry_id=current_user.id).scalar() or 0

    if total_penalty <= 0:
        flash("No penalty to offset.", "info")
        return redirect(url_for('dashboard'))

    # 2. Get Available Credits (Blockchain Balance)
    try:
        balance = float(web3_utils.get_token_balance(current_user.wallet_address))
    except Exception as e:
        flash(f"Error fetching balance: {e}", "danger")
        return redirect(url_for('dashboard'))

    # 3. Check if sufficient balance
    if balance < total_penalty:
        flash(f"Insufficient credits! You have {balance} CCT but need {total_penalty} CCT to offset penalty.", "warning")
        return redirect(url_for('dashboard'))

    # 4. Burn Tokens & Update DB
    try:
        # 0. Ensure ETH for gas
        if not web3_utils.check_and_fund_wallet(current_user.wallet_address):
            flash("Failed to fund wallet for gas fees. Contact Admin.", "danger")
            return redirect(url_for('dashboard'))

        # Burn from blockchain
        tx_hash = web3_utils.burn_tokens(
            current_user.private_key,
            total_penalty
        )

        # Clear penalties in DB
        emissions = Emission.query.filter_by(industry_id=current_user.id).all()
        for e in emissions:
            e.penalty = 0
            e.status = "Approved" # Status update to reflect compliance
        
        db.session.commit()

        flash(f"Success! {total_penalty} CCT burned to offset penalty. Tx: {tx_hash}", "success")

    except Exception as e:
        flash(f"Offset failed: {str(e)}", "danger")

    return redirect(url_for('dashboard'))

@app.route('/network')
@login_required
def industry_network():
    if current_user.role != 'industry':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industries = User.query.filter_by(role='industry').all()
    
    # Fetch real-time balances
    for ind in industries:
        try:
            if ind.wallet_address:
                balance = web3_utils.get_token_balance(ind.wallet_address)
                ind.blockchain_balance = float(balance)
            else:
                ind.blockchain_balance = 0.0
        except:
            ind.blockchain_balance = 0.0
            
    return render_template('network.html', industries=industries)

@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    import numpy as np
    from sklearn.linear_model import LinearRegression

    if current_user.role != 'industry':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    predicted_value = None
    input_year = None
    input_emission = None

    from datetime import datetime
    current_year = datetime.now().year

    if request.method == 'POST':
        try:
            input_year = int(request.form.get('year'))
            input_emission = float(request.form.get('emission'))

            if input_year <= current_year:
                flash(f"Year must be greater than {current_year}. Please enter a future year.", "danger")
                return redirect(url_for('prediction'))

            # Fetch historical emission data for this industry
            records = Emission.query.filter_by(industry_id=current_user.id).order_by(Emission.year).all()

            # Aggregate: average emissions per year (handles multiple records/year)
            from collections import defaultdict
            year_totals = defaultdict(list)
            for r in records:
                year_totals[r.year].append(r.reported_amount)

            agg_years = sorted(year_totals.keys())
            agg_emissions = [sum(year_totals[y]) / len(year_totals[y]) for y in agg_years]

            if len(agg_years) >= 2:
                # Calculate average year-over-year percentage change
                pct_changes = []
                for i in range(1, len(agg_emissions)):
                    if agg_emissions[i - 1] != 0:
                        change = (agg_emissions[i] - agg_emissions[i - 1]) / agg_emissions[i - 1]
                        pct_changes.append(change)

                if pct_changes:
                    avg_growth_rate = sum(pct_changes) / len(pct_changes)
                else:
                    avg_growth_rate = 0.03  # default 3%

                # Project from current input emission using compound growth
                years_ahead = input_year - current_year
                predicted_value = round(input_emission * ((1 + avg_growth_rate) ** years_ahead), 2)

                # Ensure prediction doesn't go negative
                if predicted_value < 0:
                    predicted_value = 0.0
            else:
                # Fallback: use 3% annual compound growth
                years_ahead = input_year - current_year
                predicted_value = round(input_emission * ((1.03) ** years_ahead), 2)

        except Exception as e:
            flash(f"Prediction error: {str(e)}", "danger")

    # Get historical records for chart (aggregated by year)
    records = Emission.query.filter_by(industry_id=current_user.id).order_by(Emission.year).all()
    from collections import defaultdict
    year_map = defaultdict(list)
    for r in records:
        year_map[r.year].append(r.reported_amount)
    history_years = sorted(year_map.keys())
    history_emissions = [round(sum(year_map[y]) / len(year_map[y]), 2) for y in history_years]

    return render_template('prediction.html',
                           predicted_value=predicted_value,
                           input_year=input_year,
                           input_emission=input_emission,
                           history_years=history_years,
                           history_emissions=history_emissions)


# ============================================================
# ================= DATA VERIFICATION (ADMIN) ================
# ============================================================

@app.route('/admin/data_verification')
@login_required
def data_verification():
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    # Get all industries that have uploaded documents
    industries_with_docs = db.session.query(User).join(EmissionDocument).distinct().all()

    # Attach document counts
    for ind in industries_with_docs:
        ind.pending_count = EmissionDocument.query.filter_by(
            industry_id=ind.id, status='PENDING VERIFICATION'
        ).count()
        ind.total_docs = EmissionDocument.query.filter_by(industry_id=ind.id).count()

    return render_template('admin_dashboard.html',
                           data_verification_mode=True,
                           industries_with_docs=industries_with_docs)


@app.route('/admin/data_verification/<int:industry_id>')
@login_required
def view_industry_documents(industry_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    industry = User.query.get_or_404(industry_id)
    documents = EmissionDocument.query.filter_by(industry_id=industry_id).order_by(EmissionDocument.uploaded_at.desc()).all()

    # Also get industries list for sidebar
    industries_with_docs = db.session.query(User).join(EmissionDocument).distinct().all()
    for ind in industries_with_docs:
        ind.pending_count = EmissionDocument.query.filter_by(
            industry_id=ind.id, status='PENDING VERIFICATION'
        ).count()
        ind.total_docs = EmissionDocument.query.filter_by(industry_id=ind.id).count()

    return render_template('admin_dashboard.html',
                           data_verification_mode=True,
                           industries_with_docs=industries_with_docs,
                           selected_industry=industry,
                           documents=documents)


@app.route('/admin/verify_document/<int:doc_id>', methods=['POST'])
@login_required
def verify_document(doc_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    doc = EmissionDocument.query.get_or_404(doc_id)
    action = request.form.get('action')  # 'approve' or 'reject'

    from datetime import datetime
    if action == 'approve':
        doc.status = 'APPROVED'
        doc.reviewed_at = datetime.utcnow()
        flash(f"Document '{doc.original_name}' approved.", "success")
    elif action == 'reject':
        doc.status = 'REJECTED'
        doc.reviewed_at = datetime.utcnow()
        flash(f"Document '{doc.original_name}' rejected.", "warning")

    db.session.commit()

    return redirect(url_for('view_industry_documents', industry_id=doc.industry_id))


@app.route('/admin/verify_industry/<int:industry_id>', methods=['POST'])
@login_required
def verify_industry_docs(industry_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('dashboard'))

    action = request.form.get('action')  # 'approve' or 'reject'
    industry = User.query.get_or_404(industry_id)
    pending_docs = EmissionDocument.query.filter_by(
        industry_id=industry_id, status='PENDING VERIFICATION'
    ).all()

    from datetime import datetime
    if action == 'approve':
        for doc in pending_docs:
            doc.status = 'APPROVED'
            doc.reviewed_at = datetime.utcnow()
        # Approve the industry's emissions
        pending_emissions = Emission.query.filter_by(
            industry_id=industry_id, status='Pending'
        ).all()
        for em in pending_emissions:
            em.status = 'Approved'
        flash(f"All documents for '{industry.username}' approved. Emissions allowed.", "success")
    elif action == 'reject':
        for doc in pending_docs:
            doc.status = 'REJECTED'
            doc.reviewed_at = datetime.utcnow()
        # Reject the industry's emissions
        pending_emissions = Emission.query.filter_by(
            industry_id=industry_id, status='Pending'
        ).all()
        for em in pending_emissions:
            em.status = 'Rejected'
        flash(f"All documents for '{industry.username}' rejected. Emissions blocked.", "warning")

    db.session.commit()

    return redirect(url_for('data_verification'))
