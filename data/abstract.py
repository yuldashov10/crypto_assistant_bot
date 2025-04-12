import abc


class Storage(abc.ABC):
    """Абстрактный базовый класс для хранилищ данных."""

    @abc.abstractmethod
    def add_purchase(
        self, user_id: int, asset: str, price: float, amount: float
    ) -> None:
        pass

    @abc.abstractmethod
    def get_purchases(
        self, user_id: int, asset: str
    ) -> list[dict[str, float]]:
        pass

    @abc.abstractmethod
    def get_user_assets(self, user_id: int) -> list[str]:
        pass

    @abc.abstractmethod
    def clear(self, user_id: int, asset: str = None) -> None:
        pass

    @abc.abstractmethod
    def delete_purchase(
        self,
        user_id: int,
        asset: str,
        purchase_index: int,
    ) -> None:
        pass


class ExportData(abc.ABC):
    """Абстрактный базовый класс для экспорта данных в файл."""

    @abc.abstractmethod
    def export_to_csv(self, user_id: int) -> list[dict[str, str]]:
        pass
