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
└── validator_router.py

STEP 0 — CLEAN START (VERY IMPORTANT)

Always reset before demo.

Command:

cd /d E:\mlops-ingestion-lab
docker compose down -v
docker compose up -d
docker ps

Why:

Clears old messages

Resets consumer offsets

Avoids demo confusion

STEP 1 — OPEN REDPANDA CONSOLE

Open browser:

http://localhost:8080

Check:

UI loads

Cluster is visible

STEP 2 — CREATE TOPICS

OPTION A: Using UI
Redpanda Console → Topics → Create Topic

Create:

orders_raw

orders_good

orders_bad

OPTION B: Using Kafka CLI (inside container)

docker exec -it kafka bash
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_raw --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_good --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --topic orders_bad --partitions 1 --replication-factor 1
exit

STEP 3 — PRODUCE RAW EVENTS

Open terminal:

cd /d E:\mlops-ingestion-lab
python scripts\ingestor_a.py
python scripts\ingestor_b.py

What happens:

Sends valid + invalid events

Publishes everything to orders_raw

Verify:
Redpanda Console → Topics → orders_raw → Messages

STEP 4 — START VALIDATOR (PANDERA)

Open NEW terminal:

cd /d E:\mlops-ingestion-lab
python scripts\validator_router.py

What happens:

Consumes orders_raw

Applies Pandera rules

Routes records:
valid → orders_good
invalid → orders_bad

STEP 5 — VERIFY ROUTING IN UI

Check GOOD data:
Topics → orders_good → Messages

Check BAD data:
Topics → orders_bad → Messages

STEP 6 — VERIFY CONSUMER HEALTH

Redpanda Console → Consumer Groups

Expected:

validator-group

State: Stable

Lag: 0

This proves pipeline health.

OPTIONAL — KAFKA CLI VERIFICATION

Run ONLY inside Kafka container.

Consume RAW:
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic orders_raw --from-beginning --timeout-ms 4000

Consume GOOD:
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic orders_good --from-beginning --timeout-ms 4000

Consume BAD:
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic orders_bad --from-beginning --timeout-ms 4000

NOTE:
Do NOT run kafka-console-consumer from Windows host using kafka:9092.

CODE OVERVIEW

ingestor_a.py

Produces mostly valid events

Writes to orders_raw

ingestor_b.py

Produces dirty / invalid events

Writes to orders_raw

validator_router.py

Kafka consumer (group: validator-group)

Uses Pandera schema

Routes records to good / bad topics

Commits offsets

PANDERA VALIDATION

Pandera enforces:

Required fields

Data types

Value constraints (amount > 0)

Allowed values (country set)

Custom business rules

IMPORTANT:
Kafka / Redpanda broker does NOT validate payloads.
Validation happens in consumer / processing layer.

REDPANDA CONSOLE — WHAT EACH TAB IS FOR

Overview : Cluster health
Topics : Data flow proof
Messages : Inspect payloads
Consumer Groups : Pipeline health + lag
Schema Registry : Schema versioning (optional)
Connect : Data pipelines
Security : RBAC / ACLs (Admin API needed)

TROUBLESHOOTING

Problem: Raw has data but good/bad is empty
Cause:

Validator not running

Offsets already committed

Wrong topic/broker

Fix:
docker compose down -v
docker compose up -d
Then rerun producers + validator.

FINAL DEMO STORY (ONE-LINERS)

Raw data is never trusted

Schema + quality checks happen in processing layer

Clean data moves forward

Bad data is quarantined

Consumer lag proves pipeline health

END OF FILE