from hedera import (
    Client, AccountId, PrivateKey,
    TokenCreateTransaction, TokenType, TokenSupplyType
)
from dotenv import load_dotenv
import os

load_dotenv()

client = Client.for_testnet()
client.set_operator(
    AccountId.fromString(os.getenv("OPERATOR_ID")),
    PrivateKey.fromString(os.getenv("OPERATOR_KEY"))
)

# Create token
token_tx = (
    TokenCreateTransaction()
    .set_token_name("DataAccessToken")
    .set_token_symbol("DAT")
    .set_token_type(TokenType.FUNGIBLE_COMMON)
    .set_initial_supply(1000)
    .set_supply_type(TokenSupplyType.INFINITE)
    .freeze_with(client)
)

sign = client.operator_private_key.sign_transaction(token_tx)
response = token_tx.execute(client)
receipt = response.get_receipt(client)
token_id = receipt.token_id
print(f"✅ Created HTS Token: {token_id}")
