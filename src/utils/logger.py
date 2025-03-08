import logging

class EndpointFilter(logging.Filter):
    def __init__(
        self,
        path: str,
        *args: any,
        **kwargs: any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1



formatter = logging.Formatter("%(asctime)s  %(levelname)s: %(message)s")
logHandler = logging.StreamHandler()
logHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(path="/livez/"))
uvicorn_logger.addFilter(EndpointFilter(path="/healthz/"))
uvicorn_logger.addFilter(EndpointFilter(path="/readyz/"))
