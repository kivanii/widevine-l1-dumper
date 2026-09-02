"""Logging configuration and utilities."""

import logging
import logging.handlers
import os
from datetime import datetime


class Logger:
    """Configure and manage logging."""

    _initialized = False
    _logger = None

    @staticmethod
    def setup(
        log_level: str = "INFO",
        log_file: str = None,
        console_output: bool = True
    ) -> logging.Logger:
        """Setup logging configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (if None, logs to console only)
            console_output: Whether to output to console
            
        Returns:
            Configured logger instance
        """
        if Logger._initialized:
            return Logger._logger

        logger = logging.getLogger("widevine_dumper")
        logger.setLevel(getattr(logging, log_level.upper()))

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        # File handler
        if log_file:
            os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        Logger._initialized = True
        Logger._logger = logger
        return logger

    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        """Get logger instance.
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if not Logger._initialized:
            Logger.setup()
        
        if name:
            return logging.getLogger(f"widevine_dumper.{name}")
        return Logger._logger
