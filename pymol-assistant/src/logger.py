import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    def __init__(self, log_file: str, 
                 log_level: int = logging.DEBUG,
                 max_bytes: int = 1_000_000, backup_count: int = 3):
        """
        Initialize the logger.

        :param log_file: Path to the log file.
        :param log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to DEBUG.
        :param max_bytes: Maximum size of a log file before rotating (default is 1MB).
        :param backup_count: Number of backup log files to keep.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Formatter to include timestamp, log level, and message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)

        # Add only the file handler to the logger
        self.logger.addHandler(file_handler)

        # Prevent duplicate log entries
        self.logger.propagate = False

        # Store the file handler to flush manually if needed
        self.file_handler = file_handler

    def log(self, message):
        self.logger.debug(message)
        self.file_handler.flush()  # Force flush to write immediately to file

    def error(self, message):
        self.logger.error(message)
        self.file_handler.flush()

    def info(self, message):
        self.logger.info(message)
        self.file_handler.flush()

    def warning(self, message):
        self.logger.warning(message)
        self.file_handler.flush()

    def critical(self, message):
        self.logger.critical(message)
        self.file_handler.flush()
