import logging
from utils.config_data import root_path
import os
from datetime import datetime


LOG_ROOT = root_path("log")
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

DEFAULT_LOG_FORMAT = logging.Formatter(
    fmt='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(
        name: str,
        level=logging.INFO,
        file_level=logging.INFO,
        stream_level=logging.INFO,
        formatter: logging.Formatter = DEFAULT_LOG_FORMAT,
        enable_file: bool = True,
        enable_stream: bool = True,
        mode='a',
        encoding='utf-8',
        delay=False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    if enable_stream:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(stream_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if enable_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, mode=mode, encoding=encoding, delay=delay)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = get_logger("app")
