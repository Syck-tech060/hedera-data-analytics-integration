import json, os
from hedera import (
    Client, AccountId, PrivateKey, TopicMessageSubmitTransaction
)
from dotenv import load_dotenv

load_dotenv()

client = Client.for_testnet()
client.set_operator(
    AccountId.fromString(os.getenv("OPERATOR_ID")),
    PrivateKey.fromString(os.getenv("OPERATOR_KEY"))
)

# Use same HCS topic or create new one for compliance
topic_id = "0.0.7148830"  # Replace with your real topic ID from ingest script

report = {
    "event": "AnomalyDetected",
    "dataset": "sales_data",
    "details": "Detected outlier values exceeding threshold",
}

tx = (
    TopicMessageSubmitTransaction()
    .set_topic_id(topic_id)
    .set_message(json.dumps(report))
    .execute(client)
)

print("✅ Compliance report submitted to HCS.")
