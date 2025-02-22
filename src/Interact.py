from web3 import Web3
from Deploy import deploy_contract
import os

contract_file = "./src/newContract.sol"
contract_name= 'newContract'
account = os.getenv("ANVIL_ACCOUNT")
private_key = os.getenv("ANVIL_PRIVATE_KEY")
provider = os.getenv("LOCAL_PROVIDER")
chain_id = 31337

connection = Web3(Web3.HTTPProvider(provider))

contract_address, abi = deploy_contract(contract_file,"newContract",account,private_key,provider,chain_id)
print(f"Contract deployed at {contract_address}")

simple_storage = connection.eth.contract(address=contract_address, abi=abi)
nonce = connection.eth.get_transaction_count(account)

print("Creating Transactions")
transaction = simple_storage.functions.updateID(5341).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": connection.eth.gas_price,
        "from": account,
        "nonce": nonce

    }
)
signed_txn = connection.eth.account.sign_transaction(transaction, private_key=private_key)

print("Updating stored Value")
tx_hash = connection.eth.send_raw_transaction(signed_txn.raw_transaction)

tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
print("updated")
updated_value = simple_storage.functions.viewMyId().call()
print(f"Updated value is {updated_value}")