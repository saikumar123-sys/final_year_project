from app import app
from models import User, MarketOrder, Emission
from web3_utils import get_token_balance, get_allowance, get_admin_address
import sys

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    print("\n=== SYSTEM STATE DIAGNOSTIC ===")
    
    admin_addr = get_admin_address()
    print(f"Admin Address: {admin_addr}")
    
    print("\n--- USERS ---")
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id} | User: {u.username} | Role: {u.role}")
        print(f"  Wallet: {u.wallet_address}")
        
        if u.role == 'industry':
            try:
                bal = get_token_balance(u.wallet_address)
                print(f"  Blockchain Balance: {bal}")
                
                allowance = get_allowance(u.wallet_address, admin_addr)
                print(f"  Allowance to Admin: {allowance}")
                
                # Check DB emissions
                total_earned = db.session.query(db.func.sum(Emission.credits_earned)).filter_by(industry_id=u.id).scalar() or 0
                print(f"  DB Earned Credits: {total_earned}")
                
            except Exception as e:
                print(f"  Error fetching blockchain data: {e}")

    print("\n--- OPEN ORDERS ---")
    orders = MarketOrder.query.filter_by(status='Open').all()
    for o in orders:
        seller = User.query.get(o.seller_id)
        print(f"Order #{o.id} | Seller: {seller.username} | Amount: {o.amount}")
        try:
            current_bal = get_token_balance(seller.wallet_address)
            print(f"  Seller Current Balance: {current_bal}")
            if float(current_bal) < o.amount:
                 print("  [WARNING] INSUFFICIENT BALANCE")
            else:
                 print("  [OK] Balance sufficient")
        except:
            print("  [ERROR] Could not check balance")

    print("\n=== END DIAGNOSTIC ===")
