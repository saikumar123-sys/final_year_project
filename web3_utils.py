import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

# Connect to Blockchain (Ganache or Testnet)
RPC_URL = os.getenv('RPC_URL', 'http://127.0.0.1:7545')
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Admin Wallet (Deployer)
ADMIN_ADDRESS = os.getenv('ADMIN_ADDRESS')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY')

CHAIN_ID = web3.eth.chain_id  # Automatically detect chain id

# ---------------- Contract Compilation ----------------
def compile_contract():
    try:
        install_solc('0.8.0')
    except:
        pass  # Already installed

    with open('./contracts/CarbonCredit.sol', 'r') as file:
        carbon_credit_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"CarbonCredit.sol": {"content": carbon_credit_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    bytecode = compiled_sol["contracts"]["CarbonCredit.sol"]["CarbonCredit"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"]["CarbonCredit.sol"]["CarbonCredit"]["metadata"])["output"]["abi"]

    return bytecode, abi

# ---------------- Contract Deployment ----------------
def deploy_contract():
    if not ADMIN_ADDRESS or not ADMIN_PRIVATE_KEY:
        print("Admin credentials not found. Cannot deploy.")
        return None

    bytecode, abi = compile_contract()
    
    # Save ABI locally
    with open("CarbonCredit_abi.json", "w") as f:
        json.dump(abi, f)

    CarbonCredit = web3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)

    transaction = CarbonCredit.constructor().build_transaction({
        "chainId": CHAIN_ID,
        "from": ADMIN_ADDRESS,
        "nonce": nonce,
        "gasPrice": web3.eth.gas_price
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=ADMIN_PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt.contractAddress

# ---------------- Get Contract ----------------
def get_contract():
    contract_address = os.getenv("CONTRACT_ADDRESS")
    if not contract_address:
        raise Exception("CONTRACT_ADDRESS not set in .env")

    with open("CarbonCredit_abi.json", "r") as f:
        abi = json.load(f)

    return web3.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=abi
    )

# ---------------- Create Wallet for New Industry ----------------
def create_wallet():
    """
    Generate a new Ethereum wallet for an industry
    Returns: (address, private_key)
    """
    account = web3.eth.account.create()
    return account.address, account.key.hex()

# ---------------- Mint / Burn / Transfer / Approve ----------------
def mint_tokens(to_address, amount):
    contract = get_contract()
    amount_wei = web3.to_wei(amount, 'ether')
    nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
    tx = contract.functions.mint(to_address, amount_wei).build_transaction({
        'chainId': CHAIN_ID,
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gasPrice': web3.eth.gas_price
    })
    signed_txn = web3.eth.account.sign_transaction(tx, private_key=ADMIN_PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def get_token_balance(address):
    contract = get_contract()
    balance = contract.functions.balanceOf(address).call()
    return web3.from_wei(balance, 'ether')

def burn_tokens(private_key, amount):
    contract = get_contract()
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    amount_wei = web3.to_wei(amount, 'ether')
    tx = contract.functions.burn(amount_wei).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.to_hex(tx_hash)

def get_admin_address():
    if not ADMIN_PRIVATE_KEY:
        return os.getenv('ADMIN_ADDRESS')
    try:
        account = web3.eth.account.from_key(ADMIN_PRIVATE_KEY)
        return account.address
    except:
        return os.getenv('ADMIN_ADDRESS')

def approve_tokens(owner_private_key, amount):
    contract = get_contract()
    owner_account = web3.eth.account.from_key(owner_private_key)
    admin_address = get_admin_address()
    nonce = web3.eth.get_transaction_count(owner_account.address)
    amount_wei = web3.to_wei(amount, 'ether')
    tx = contract.functions.approve(admin_address, amount_wei).build_transaction({
        'from': owner_account.address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, owner_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.to_hex(tx_hash)

def get_allowance(owner_address, spender_address):
    contract = get_contract()
    allowance = contract.functions.allowance(owner_address, spender_address).call()
    return web3.from_wei(allowance, 'ether')

def check_and_fund_wallet(address):
    """
    Checks if wallet has enough ETH for gas. If not, funds it from Admin.
    """
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_eth = float(web3.from_wei(balance_wei, 'ether'))
        
        # Threshold: 0.01 ETH
        if balance_eth < 0.01:
            print(f"Low ETH balance ({balance_eth}). Funding wallet {address}...")
            if not ADMIN_PRIVATE_KEY:
                print("Cannot fund: Admin private key missing")
                return False
                
            nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
            tx = {
                'to': address,
                'value': web3.to_wei(0.05, 'ether'), # Fund 0.05 ETH
                'gas': 21000,
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce,
                'chainId': CHAIN_ID
            }
            signed_tx = web3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Funded {address} with 0.05 ETH. Tx: {web3.to_hex(tx_hash)}")
            return True
        return True
    except Exception as e:
        print(f"Funding check failed: {e}")
        return False

def transfer_tokens(from_address, to_address, amount):
    contract = get_contract()
    admin_private_key = os.getenv("ADMIN_PRIVATE_KEY")
    admin_account = web3.eth.account.from_key(admin_private_key)
    amount_wei = web3.to_wei(amount, 'ether')
    seller_balance = contract.functions.balanceOf(from_address).call()
    if seller_balance < amount_wei:
        raise Exception("Blockchain: Seller does not have enough credits")
    allowance = contract.functions.allowance(from_address, admin_account.address).call()
    if allowance < amount_wei:
        raise Exception("Seller has not approved enough credits for exchange settlement")
    nonce = web3.eth.get_transaction_count(admin_account.address)
    tx = contract.functions.transferFrom(from_address, to_address, amount_wei).build_transaction({
        'from': admin_account.address,
        'nonce': nonce,
        'gas': 500000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, admin_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        raise Exception("Blockchain transaction reverted")
    return web3.to_hex(tx_hash)
