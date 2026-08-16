from web3_utils import deploy_contract

if __name__ == "__main__":
    address = deploy_contract()
    print("\n✅ Contract deployed successfully")
    print("📌 Contract Address:", address)
