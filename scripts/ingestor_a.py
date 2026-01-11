import json
import time
from kafka import KafkaProducer

BOOTSTRAP = "localhost:29092"
TOPIC = "orders_raw"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=5,
)

events = [
    {"order_id": 1, "user_id": 101, "amount": 499.0, "country": "IN", "channel": "web"},     # ✅
    {"order_id": 2, "user_id": 102, "amount": -10.0, "country": "US", "channel": "app"},     # ❌
    {"order_id": 3, "user_id": 103, "amount": 199.0, "country": "UK", "channel": "partner"}, # ✅
]

for e in events:
    producer.send(TOPIC, e)
    print("[A] sent:", e)
    time.sleep(0.4)

producer.flush()
print("[A] done")
