import logging

from .abstract import Storage
from .storage import JSONStorage, MemoryStorage, SQLiteStorage
from core.logging import LoggerConfig

logger = LoggerConfig(
    logger_name="factory",
    log_file="cab.log",
    log_level=logging.DEBUG,
).get_logger()


class StorageFactory:
    """Фабрика для создания хранилищ данных."""

    @staticmethod
    def create_storage(storage_type: str, **kwargs) -> Storage:
        if storage_type == "memory":
            return MemoryStorage()
        elif storage_type == "sqlite":
            return SQLiteStorage(db_path=kwargs.get("db_path", "cab.db"))
        elif storage_type == "json":
            return JSONStorage(file_path=kwargs.get("file_path", "cab.json"))

        logger.error(f"Неизвестный тип хранилища: {storage_type}")
        raise TypeError(f"Неизвестный тип хранилища: {storage_type}")
