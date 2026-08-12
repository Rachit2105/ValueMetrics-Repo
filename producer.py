"""RabbitMQ producer for mutual-fund processing jobs."""
import json
from pathlib import Path

import pika

from config import settings
from logging_config import get_logger

logger = get_logger(__name__)


def publish_job(file_path: str, save_file_path: str) -> None:
    """Publish one processing job to RabbitMQ."""
    input_path = Path(file_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.rabbitmq_host)
    )
    try:
        channel = connection.channel()
        channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
        channel.confirm_delivery()

        payload = {
            "file_path": str(input_path),
            "save_file_path": str(Path(save_file_path)),
        }

        channel.basic_publish(
            exchange="",
            routing_key=settings.rabbitmq_queue,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
            mandatory=True,
        )
        logger.info("Published processing job for %s", input_path)
    finally:
        connection.close()


if __name__ == "__main__":
    publish_job("AMCdata.csv", "FormattedData.xlsx")
