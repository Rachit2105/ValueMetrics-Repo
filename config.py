"""Application configuration for the mutual-fund processing pipeline."""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_queue: str = os.getenv("RABBITMQ_QUEUE", "mutual_fund_processing")
    rabbitmq_prefetch: int = int(os.getenv("RABBITMQ_PREFETCH", "1"))


settings = Settings()
