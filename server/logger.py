import logging
import sys


class ColoredFormatter:
    """Простой цветной форматтер. Создает все форматтеры заранее."""

    COLORS = {
        logging.DEBUG: "\x1b[38;21m",      # Grey
        logging.INFO: "\x1b[38;5;39m",     # Blue
        logging.WARNING: "\x1b[38;5;226m",  # Yellow
        logging.ERROR: "\x1b[38;5;196m",   # Red
        logging.CRITICAL: "\x1b[31;1m",    # Bold Red
    }
    RESET = "\x1b[0m"

    def __init__(self, fmt):
        self.fmt = fmt

        # Сразу создадим все объекты форматтеров для всех уровней,
        # чтобы не создавать экземпляр форматтера при каждом запросе
        self._formatters = {}
        for level, color in self.COLORS.items():
            self._formatters[level] = logging.Formatter(
                f"{color}{fmt}{self.RESET}"
            )

    def format(self, record):
        return self._formatters[record.levelno].format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": ColoredFormatter,
            "fmt": "[%(asctime)s] [%(levelname)s] - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "request": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        }
    }
}


def setup_logging():
    """Настраиваем логирование."""
    import logging.config
    logging.config.dictConfig(LOGGING_CONFIG)
