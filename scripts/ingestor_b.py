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
    {"order_id": 10, "user_id": None, "amount": 99.0, "country": "IN", "channel": "web"},   # ❌
    {"order_id": 11, "user_id": 201, "amount": 150.0, "country": "FR", "channel": "web"},   # ❌
    {"order_id": 12, "user_id": 202, "amount": 250.0, "country": "US", "channel": "app"},   # ✅
]
#   if API Is Called then Send Data VIA Producer 
for e in events:
    producer.send(TOPIC, e)
    print("[B] sent:", e)
    time.sleep(0.4)

producer.flush()
print("[B] done")


