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