import pandas as pd
import hashlib, json, os
from hedera import (
    Client,
    AccountId,
    PrivateKey,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction
)
from dotenv import load_dotenv

load_dotenv()

client = Client.for_testnet()
client.set_operator(
    AccountId.fromString(os.getenv("OPERATOR_ID")),
    PrivateKey.fromString(os.getenv("OPERATOR_KEY"))
)

# Create a topic for data provenance
topic_tx = TopicCreateTransaction().set_memo("Data Provenance Logs").execute(client)
topic_id = topic_tx.get_receipt(client).topic_id
print(f"✅ Created HCS Topic: {topic_id}")

# Load CSV and compute digest
df = pd.read_csv("data/sample.csv")
digest = hashlib.sha256(df.to_json().encode()).hexdigest()

log_message = {
    "filename": "sample.csv",
    "digest": digest,
    "rows": len(df),
    "source": "local_csv"
}

tx = (
    TopicMessageSubmitTransaction()
    .set_topic_id(topic_id)
    .set_message(json.dumps(log_message))
    .execute(client)
)

print(f"✅ Logged data hash to HCS: {digest[:20]}...")
