from app import app
from extensions import db
from models import User, MarketOrder
import web3_utils
import sys

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    print("--- USERS & BALANCES ---")
    users = User.query.all()
    user_map = {}
    for u in users:
        user_map[u.id] = u
        balance = "N/A"
        if u.wallet_address:
            try:
                balance = web3_utils.get_token_balance(u.wallet_address)
            except Exception as e:
                balance = f"Error: {e}"
        print(f"User: {u.username} (ID: {u.id}) | Wallet: {u.wallet_address} | Balance: {balance}")

    print("\n--- MARKET ORDERS FILTERING CHECK ---")
    all_orders = MarketOrder.query.filter_by(status='Open').all()
    print(f"Total Open Orders: {len(all_orders)}")
    
    for order in all_orders:
        seller = user_map.get(order.seller_id)
        if not seller:
            print(f"Order {order.id}: Seller not found (ID {order.seller_id}) -> SKIPPED")
            continue
            
        print(f"Order {order.id}: Seller {seller.username}, Amount {order.amount}")
        
        # Replicate logic from routes.py
        try:
            balance = float(web3_utils.get_token_balance(seller.wallet_address))
            print(f"  - Seller Balance: {balance}")
            
            if balance >= order.amount:
                print(f"  - Logic: {balance} >= {order.amount} -> INCLUDED")
            else:
                print(f"  - Logic: {balance} < {order.amount} -> EXCLUDED (Insufficient Balance)")
        except Exception as e:
            print(f"  - Logic: Error fetching balance: {e} -> SKIPPED")
