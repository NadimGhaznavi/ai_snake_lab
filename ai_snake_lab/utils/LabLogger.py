"""
ai_snake_lab/utils/LabLogger.py

    Database 4 Everything
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/db4e
    License: GPL 3.0

"""

import logging

from ai_snake_lab.constants.DLabLogger import DLog, LOG_LEVELS


class LabLogger:
    def __init__(self, client_id: str, log_file=None, to_console=True):
        self._logger = logging.getLogger(client_id)

        # Set the logger log level, should always be 'debug'
        self._logger.setLevel(LOG_LEVELS[DLog.DEBUG])

        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Optional file handler
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(LOG_LEVELS[DLog.DEBUG])
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        # Optional console handler
        if to_console:
            ch = logging.StreamHandler()
            ch.setLevel(LOG_LEVELS[DLog.DEBUG])
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)

        self._logger.propagate = False

    def shutdown(self):
        # Exit cleanly
        logging.shutdown()  # Flush all handlers

    # Basic log message handling, wraps Python's logging object
    def info(self, message, extra=None):
        self._logger.info(message, extra=extra)

    def debug(self, message, extra=None):
        self._logger.debug(message, extra=extra)

    def warning(self, message, extra=None):
        self._logger.warning(message, extra=extra)

    def error(self, message, extra=None):
        self._logger.error(message, extra=extra)

    def critical(self, message, extra=None):
        self._logger.critical(message, extra=extra)
