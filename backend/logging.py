import logging
import os

import colorlog
from backend.core.constants.log_color import LogColor


def configure_application():
    """Apply config"""

    def configure_logging():
        """Configure the base logger for the application."""
        root_logger = logging.getLogger()

        # If logger exists
        if root_logger.handlers:
            logging.debug("Logger already configured. Skipping reconfiguration.")
            return

        log_level = os.getenv("APP_LOG_LEVEL", "INFO")
        root_logger.setLevel(log_level)

        colored_formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s] - %(levelname)s - %(process)d - %(name)s:%(lineno)d:%(reset)s %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
            log_colors={
                "DEBUG": LogColor.DEBUG,
                "INFO": LogColor.INFO,
                "WARNING": LogColor.WARNING,
                "ERROR": LogColor.ERROR,
                "CRITICAL": LogColor.CRITICAL,
            },
            secondary_log_colors={},
            style="%",
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(colored_formatter)
        root_logger.addHandler(stream_handler)
        logging.info("Logging configured with level: %s", log_level)

    configure_logging()
