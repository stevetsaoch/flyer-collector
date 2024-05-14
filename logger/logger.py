# loguru
from loguru import logger

LOG_PATH: str = "./log"

logger.add(
    LOG_PATH,
    format="{time} | {level} | {extra[instance_name]} | {message}",
    level="DEBUG",
    rotation="1 day",
    retention="10 days",
    enqueue=True,
)
