from app import app
from extensions import db
from models import User, Emission, MarketOrder, CreditRetirement
from web3_utils import (
    web3, get_token_balance, mint_tokens, approve_tokens, 
    get_allowance, get_admin_address, ADMIN_ADDRESS
)
import sys

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

def sync_industry_data():
    with app.app_context():
        print("\n=== STARTING DATA SYNCHRONIZATION ===")
        
        industries = User.query.filter_by(role='industry').all()
        admin_addr = get_admin_address()
        
        for user in industries:
            print(f"\nProcessing: {user.username} ({user.wallet_address})")
            
            # --- 1. Calculate Expected Balance from DB History ---
            # Earned from Emissions
            total_earned = db.session.query(db.func.sum(Emission.credits_earned))\
                .filter_by(industry_id=user.id).scalar() or 0
                
            # Sold in Market (Completed)
            total_sold = db.session.query(db.func.sum(MarketOrder.amount))\
                .filter_by(seller_id=user.id, status='Completed').scalar() or 0
                
            # Bought in Market (Completed)
            total_bought = db.session.query(db.func.sum(MarketOrder.amount))\
                .filter_by(buyer_id=user.id, status='Completed').scalar() or 0
                
            # Retired (Offset)
            total_retired = db.session.query(db.func.sum(CreditRetirement.credits_retired))\
                .filter_by(industry_id=user.id).scalar() or 0
                
            # Also check penalty offsets that might have burned tokens directly without a Retirement record
            # (In our current logic, we update Emission.penalty=0, so relying on that might be tricky if not logged elsewhere)
            # For now, let's assume offsets are tracked or penalties are handled.
            
            expected_balance = (total_earned + total_bought) - (total_sold + total_retired)
            print(f"  DB History -> Earned: {total_earned}, Bought: {total_bought}, Sold: {total_sold}, Retired: {total_retired}")
            print(f"  Expected Balance: {expected_balance}")
            
            if expected_balance < 0:
                print("  [WARNING] Expected balance is negative! DB data might be inconsistent.")
                expected_balance = 0 # Safety floor
            
            # --- 2. Check Actual Blockchain Balance ---
            try:
                current_balance_wei = web3.eth.get_balance(user.wallet_address)
                # Ensure ETH for gas first
                if current_balance_wei < web3.to_wei(0.01, 'ether'):
                     print("  Funding gas...")
                     # Fund code copied from fix scripts
                     nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
                     tx = {
                        'to': user.wallet_address,
                        'value': web3.to_wei(0.1, 'ether'),
                        'gas': 21000,
                        'gasPrice': web3.eth.gas_price,
                        'nonce': nonce,
                        'chainId': web3.eth.chain_id
                     }
                     # We need admin private key here
                     from web3_utils import ADMIN_PRIVATE_KEY
                     signed = web3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
                     web3.eth.send_raw_transaction(signed.raw_transaction)
                     print("  Gas Funded.")

                actual_balance = float(get_token_balance(user.wallet_address))
                print(f"  Actual Blockchain Balance: {actual_balance}")
                
                # --- 3. Reconcile (Mint if missing) ---
                if actual_balance < expected_balance:
                    diff = expected_balance - actual_balance
                    if diff > 0.000001: # float tolerance
                        print(f"  [FIX] Minting {diff} CCT to restore balance...")
                        mint_tx = mint_tokens(user.wallet_address, diff)
                        print(f"  Mint Success! Tx: {mint_tx}")
                    else:
                        print("  Balance matches (within tolerance).")
                else:
                    print("  Balance is sufficient (or higher). No action needed.")
                    
                # --- 4. Fix Allowance (For Trading) ---
                # Check if they have open sell orders
                open_orders = MarketOrder.query.filter_by(seller_id=user.id, status='Open').all()
                total_for_sale = sum(o.amount for o in open_orders)
                
                if total_for_sale > 0:
                    print(f"  Open Orders Total: {total_for_sale}")
                    current_allowance = float(get_allowance(user.wallet_address, admin_addr))
                    print(f"  Current Allowance: {current_allowance}")
                    
                    if current_allowance < total_for_sale:
                        print("  [FIX] Allowance too low. Approving max...")
                        # We need user private key. In this demo/dev env, we might have it in DB?
                        # models.py shows `private_key` field.
                        if user.private_key:
                            approve_tx = approve_tokens(user.private_key, 1000000.0) # Approve large amount
                            print(f"  Approval Success! Tx: {approve_tx}")
                        else:
                            print("  [ERROR] User private key missing in DB. Cannot approve.")
                
            except Exception as e:
                print(f"  [ERROR] Sync failed for {user.username}: {e}")
                import traceback
                traceback.print_exc()

        print("\n=== SYNCHRONIZATION COMPLETE ===")

if __name__ == "__main__":
    sync_industry_data()
