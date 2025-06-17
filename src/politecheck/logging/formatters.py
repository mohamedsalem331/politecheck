import json
import logging
from datetime import datetime
from typing import Any, Dict

class StructuredJsonFormatter(logging.Formatter):
    """Custom JSON formatter that includes timestamp and structured data."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Get the structured data from the record
        structured_data = getattr(record, 'structured', {})
        
        # Create the log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add structured data if present
        if structured_data:
            log_entry['structured'] = structured_data
            
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
            
        return json.dumps(log_entry) 