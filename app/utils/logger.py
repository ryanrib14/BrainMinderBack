from pydantic import BaseModel
from datetime import datetime
import logging
from typing import Optional, Any, Dict


class LogInfoApi(BaseModel):
    level: str
    clientId: str
    clientSlug: str
    serviceId: str
    requestId: str
    timestamp: datetime
    message: str
    metadata: Optional[Dict[str, Any]]


class LogInfoGeneral(BaseModel):
    level: str
    timestamp: datetime
    message: str
    metadata: Optional[Dict[str, Any]]


class JsonLogger:
    @staticmethod
    def log(
        level: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if headers:
            log_info = LogInfoApi(
                level=level,
                clientId=headers.get("clientId"),
                clientSlug=headers.get("clientSlug"),
                serviceId=headers.get("serviceId"),
                requestId=headers.get("requestId"),
                timestamp=datetime.now(),
                message=message,
                metadata=metadata,
            )
        else:
            log_info = LogInfoGeneral(
                level=level,
                timestamp=datetime.now(),
                message=message,
                metadata=metadata,
            )
        if level == "CRITICAL":
            logging.critical(log_info.json())
        elif level == "ERROR":
            logging.error(log_info.json())
        elif level == "WARNING":
            logging.warning(log_info.json())
        elif level == "INFO":
            logging.info(log_info.json())
        elif level == "DEBUG":
            logging.debug(log_info.json())
