from app import app
from models import User
from web3_utils import web3, approve_tokens, get_allowance, get_admin_address, ADMIN_ADDRESS, ADMIN_PRIVATE_KEY

with app.app_context():
    tata = User.query.filter(User.username.ilike('%tata%')).first()
    
    if not tata:
        print("Tata Industry not found")
        exit()
        
    if not tata.wallet_address or not tata.private_key:
        print("Tata wallet/private key missing")
        exit()

    print(f"Target: {tata.username} ({tata.wallet_address})")

    # 1. Check ETH Balance
    eth_bal_wei = web3.eth.get_balance(tata.wallet_address)
    eth_bal = web3.from_wei(eth_bal_wei, 'ether')
    print(f"ETH Balance: {eth_bal}")

    # 2. Fund if needed
    if eth_bal < 0.05:
        print("Balance too low for gas. Funding from Admin...")
        try:
            nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
            tx = {
                'to': tata.wallet_address,
                'value': web3.to_wei(0.1, 'ether'),
                'gas': 21000,
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce,
                'chainId': web3.eth.chain_id
            }
            signed = web3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Funded! Tx: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"Funding failed: {e}")
            # Try to proceed anyway? No, approval will fail.

    # 3. Approve Tokens
    print("Approving tokens for trade...")
    try:
        # Approve significantly more than the order amount (e.g. 1000)
        tx_hash = approve_tokens(tata.private_key, 1000.0)
        print(f"Approval Success! Tx: {tx_hash}")
        
    except Exception as e:
        print(f"Approval Failed: {e}")

    # 4. Verify Allowance
    try:
        admin_addr = get_admin_address()
        allowance = get_allowance(tata.wallet_address, admin_addr)
        print(f"Current Allowance: {allowance}")
    except Exception as e:
        print(f"Verification Failed: {e}")
