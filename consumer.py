"""Reliable RabbitMQ consumer for mutual-fund processing jobs."""
import json

import pika

from all_required_functions import format_data
from config import settings
from logging_config import get_logger

logger = get_logger(__name__)


def process_message(ch, method, properties, body) -> None:
    """Process one message and ACK only after successful completion."""
    try:
        data = json.loads(body)

        file_path = data["file_path"]
        save_file_path = data["save_file_path"]

        logger.info("Processing %s -> %s", file_path, save_file_path)
        format_data(file_path, save_file_path)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Job completed successfully")
    except (json.JSONDecodeError, KeyError, FileNotFoundError, ValueError, OSError) as exc:
        logger.exception("Job failed: %s", exc)
        # Reject and requeue so a transient failure can be retried.
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main() -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.rabbitmq_host)
    )
    channel = connection.channel()

    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
    channel.basic_qos(prefetch_count=settings.rabbitmq_prefetch)
    channel.basic_consume(
        queue=settings.rabbitmq_queue,
        on_message_callback=process_message,
        auto_ack=False,
    )

    logger.info("Waiting for jobs on queue '%s'...", settings.rabbitmq_queue)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
