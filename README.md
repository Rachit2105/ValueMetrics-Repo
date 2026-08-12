# Mutual Fund Data Processing Pipeline

An asynchronous Python data-processing pipeline that uses **RabbitMQ** for job delivery and **Pandas** for cleaning, classification, transformation, and Excel output.

## Architecture

CSV → Producer → RabbitMQ Queue → Consumer → Pandas ETL → Formatted Excel

## What it does

- Reads mutual-fund scheme data from CSV.
- Validates required columns.
- Normalizes scheme names.
- Classifies schemes into:
  - Direct Growth
  - Direct Dividend
  - Regular Growth
  - Regular Dividend
- Removes duplicate and uncategorized records.
- Pivots the processed data into a stable reporting format.
- Writes the final dataset to Excel.
- Uses durable RabbitMQ queues and manual acknowledgements so a job is acknowledged only after successful processing.

## Run

1. Install RabbitMQ locally and start the RabbitMQ service.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

4. Put the source CSV in the project directory.

5. Start the consumer:

```bash
python consumer.py
```

6. In another terminal, publish a job:

```bash
python producer.py
```

## Configuration

Environment variables:

- `RABBITMQ_HOST` — default: `localhost`
- `RABBITMQ_QUEUE` — default: `mutual_fund_processing`
- `RABBITMQ_PREFETCH` — default: `1`

## Project structure

```text
config.py
logging_config.py
all_required_functions.py
producer.py
consumer.py
requirements.txt
```
