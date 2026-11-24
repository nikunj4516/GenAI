"""Basic logging: console + rotating file (logs/app.log)."""
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler

from app import config

_configured = False
_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging() -> None:
    global _configured
    if _configured:
        return

    level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    formatter = logging.Formatter(_FORMAT)
    root = logging.getLogger()
    root.setLevel(level)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    try:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            config.LOG_DIR / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    except OSError as exc:  # read-only disk etc. - never crash because of logging
        root.warning("File logging disabled: %s", exc)

    for noisy in ("httpx", "httpcore", "urllib3", "sentence_transformers", "faiss"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)
