import logging
from logfire import configure, LogfireLoggingHandler, instrument_requests, instrument_sqlalchemy

_logger_initialized = False

def setup_logging():
    global _logger_initialized  # Use a global variable as the guard
    if _logger_initialized:     # Check if the logger is already initialized
        return logging.getLogger(__name__)  # Return the existing logger

    # Perform the initialization logic
    configure()
    logging.basicConfig(handlers=[LogfireLoggingHandler()])
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

     # Enable instrumentation for requests and SQLAlchemy
    instrument_requests()
    instrument_sqlalchemy()

    _logger_initialized = True  # Set the guard to True to indicate initialization is done
    return logger

if __name__ == '__main__':
    setup_logging()