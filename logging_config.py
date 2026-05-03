import logging
import logging.handlers
import json
import os
from datetime import datetime
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry, indent=None, separators=(',', ':'))

def setup_logging(log_level=logging.INFO, log_to_file=True):
    """Setup comprehensive logging configuration."""

    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Set root logger level
    root_logger.setLevel(log_level)

    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    if log_to_file:
        # Rotating file handler for general logs
        file_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "mini_devin.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        json_formatter = JSONFormatter()
        file_handler.setFormatter(json_formatter)
        root_logger.addHandler(file_handler)

        # Separate error log file
        error_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "mini_devin_error.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        root_logger.addHandler(error_handler)

        # API specific logs
        api_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "api.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        api_handler.setLevel(logging.INFO)
        api_handler.setFormatter(json_formatter)
        api_handler.addFilter(lambda record: record.name.startswith('api'))
        root_logger.addHandler(api_handler)

        # Agent specific logs
        agent_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "agent.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        agent_handler.setLevel(logging.DEBUG)
        agent_handler.setFormatter(json_formatter)
        agent_handler.addFilter(lambda record: record.name.startswith('agents'))
        root_logger.addHandler(agent_handler)

        # LLM specific logs
        llm_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "llm.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        llm_handler.setLevel(logging.INFO)
        llm_handler.setFormatter(json_formatter)
        llm_handler.addFilter(lambda record: record.name.startswith('llm'))
        root_logger.addHandler(llm_handler)

    # Create loggers for different modules
    loggers = {
        'api': logging.getLogger('api'),
        'agents': logging.getLogger('agents'),
        'llm': logging.getLogger('llm'),
        'database': logging.getLogger('database'),
        'storage': logging.getLogger('storage'),
        'ui': logging.getLogger('ui'),
    }

    return loggers

def get_logger(name):
    """Get a configured logger for a specific module."""
    return logging.getLogger(name)

# Global loggers instance
loggers = None

def init_logging(log_level=logging.INFO, log_to_file=True):
    """Initialize logging system."""
    global loggers
    loggers = setup_logging(log_level, log_to_file)
    return loggers
