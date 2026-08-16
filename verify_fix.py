from app import app
from extensions import db
from models import User, MarketOrder
import web3_utils
import sys

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    print("\n--- VERIFYING MARKET LISTING VISIBILITY ---")
    all_orders = MarketOrder.query.filter_by(status='Open').all()
    print(f"Total Open Orders: {len(all_orders)}")
    
    for order in all_orders:
        seller = User.query.get(order.seller_id)
        if not seller:
            continue
            
        print(f"Order {order.id}: Seller {seller.username}, Amount {order.amount}")
        
        # Simulate new routes.py logic
        try:
            balance = float(web3_utils.get_token_balance(seller.wallet_address))
            order.seller_balance = balance
            
            is_valid = balance >= order.amount
            
            print(f"  - Balance: {balance}")
            print(f"  - Valid? {is_valid}")
            
            if is_valid:
                print("  - Result: Visible & Buyable")
            else:
                print("  - Result: Visible but Warning (Insufficient Funds)")
                
        except Exception as e:
            print(f"  - Error: {e}")
