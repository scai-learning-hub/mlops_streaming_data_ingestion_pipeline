import json
import pandas as pd
from kafka import KafkaConsumer, KafkaProducer
import pandera as pa
from schema_orders import OrderSchema

BOOTSTRAP = "localhost:29092"

RAW_TOPIC = "orders_raw"
GOOD_TOPIC = "orders_good"
BAD_TOPIC = "orders_bad"

consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=BOOTSTRAP,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="validator-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print(f"[validator] listening: {RAW_TOPIC} -> ({GOOD_TOPIC}, {BAD_TOPIC})")

for msg in consumer:
    event = msg.value
    try:
        df = pd.DataFrame([event])

        # Validate (will raise on any bad case)
        OrderSchema.validate(df, lazy=True)

        producer.send(GOOD_TOPIC, event)
        producer.flush()
        print("✅ GOOD:", event)

    except Exception as e:
        bad_event = {
            "reason": str(e)[:200],   # keep it short
            "payload": event
        }
        producer.send(BAD_TOPIC, bad_event)
        producer.flush()
        print("❌ BAD:", bad_event)
