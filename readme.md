KAFKA INGESTION QUALITY-CONTROL LAB
(Kafka + Redpanda Console + Pandera)

GOAL OF THIS LAB

This lab demonstrates a production-style ingestion quality gate:

Raw Events → Validation → Good / Bad Routing

By the end of this lab, you will be able to DEMO:

Raw data ingestion into Kafka

Schema + data quality validation using Pandera

Routing of clean data to a GOOD topic

Quarantining of invalid data to a BAD topic

Using Redpanda Console UI to observe topics, messages, and consumer health

ARCHITECTURE OVERVIEW

Producer A
→ orders_raw → Validator (Pandera) → orders_good
Producer B / → orders_bad

TECH STACK

Kafka : Streaming backbone

Redpanda Console : Kafka UI

Python : Producers + Validator

Pandera : Data quality & schema validation

Docker Compose : Local reproducible infra

TOPICS USED

orders_raw : All incoming raw events
orders_good : Validated clean events
orders_bad : Invalid / quarantined events
__consumer_offsets : Kafka internal offsets topic

PREREQUISITES

Docker Desktop (running)

Python 3.10+

Windows CMD or PowerShell

PROJECT STRUCTURE

.
│
├── docker-compose.yml
├── requirements.txt
└── scripts
├── ingestor_a.py
├── ingestor_b.py
├── schema_orders.py
└── validator_consumer.py

STEP 0 — CLEAN START (VERY IMPORTANT)

Always reset before demo.

Command:

cd /d E:\mlops-ingestion-lab
docker compose down -v
docker compose up -d
docker ps

Why:

Clears old messages

KAFKA INGESTION LAB — Quick Reference

Purpose
- Demo a simple ingestion quality gate: raw → validate → good/bad.

Quick start
- Prereqs: Docker Desktop (running), Python 3.10+, PowerShell/CMD.
- Reset infra and start:

```powershell
cd /d E:\mlops-ingestion-lab
docker compose down -v
docker compose up -d
```

Create topics (recommended: inside the Kafka container)

```bash
docker exec -it kafka bash
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_raw --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_good --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_bad --partitions 1 --replication-factor 1
exit
```

Note: example producers in `scripts/` use `BOOTSTRAP = "localhost:29092"` (host access). If running producers inside the container, use `kafka:9092`.

Run producers

```powershell
python scripts\ingestor_a.py
python scripts\ingestor_b.py
```

Run validator

```powershell
python scripts\validator_consumer.py
```

Topics
- `orders_raw` — incoming events
- `orders_good` — validated events
- `orders_bad` — quarantined events

Files
- `scripts/ingestor_a.py` — produces mostly valid events
- `scripts/ingestor_b.py` — produces invalid/dirty events
- `scripts/schema_orders.py` — Pandera schema
- `scripts/validator_consumer.py` — validator/producer router

Troubleshooting
- If good/bad remain empty: ensure `validator_consumer.py` is running and try resetting infra:

```powershell
docker compose down -v
docker compose up -d
```

Optional verification (inside container):

```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic orders_raw --from-beginning --timeout-ms 4000
```

That's it — concise and focused. Update `requirements.txt` if you want me to add `kafka-python`, `pandas`, and `pandera`.