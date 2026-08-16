from app import app
from models import User
from web3_utils import get_token_balance, burn_tokens
import sys

# Force unbuffered output
sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    tata = User.query.filter(User.username.ilike('%tata%')).first()
    if not tata:
        print("Tata not found")
        exit()
        
    print(f"User: {tata.username}")
    current_bal = float(get_token_balance(tata.wallet_address))
    print(f"Current Balance: {current_bal}")
    
    target_bal = 500.0
    
    if current_bal > target_bal:
        diff = current_bal - target_bal
        print(f"Reducing balance by {diff} to reach {target_bal}...")
        
        if tata.private_key:
            tx = burn_tokens(tata.private_key, diff)
            print(f"Burned {diff} CCT. Tx: {tx}")
            
            new_bal = float(get_token_balance(tata.wallet_address))
            print(f"New Balance: {new_bal}")
        else:
            print("Private key inconsistent/missing")
    else:
        print(f"Balance is already {current_bal} (<= {target_bal})")
