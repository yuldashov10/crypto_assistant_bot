WELCOME: str = (
    "Привет, {name}! 👋\n\n"
    "📝 Доступные операции:\n\n"
    "/add - Добавить покупку\n"
    "/view - Посмотреть среднюю цену\n"
    "/delete - Удалить покупку\n"
    "/clear - Очистить данные\n"
    "/list - Показать список криптовалют\n"
    "/export - Экспортировать данные в CSV"
)

HELP: str = (
    "Необходимо указать: \n\t"
    "- название актива\n\t"
    "- количество монет\n\t"
    "- цену покупки\n\n"
    "ℹ Используйте /add для добавления покупки"
)


PURCHASE_INPUT_DATA: str = (
    "\n🪙 Название актива: {asset}"
    "\n💱 Цена: {price}"
    "\n⚖️ Количество: {amount}"
)

ADDED_PURCHASE_INFO: str = (
    "🛒 Покупка добавлена:\n"
    "Актив: {asset}\n"
    "Цена: {price}\n"
    "Количество: {amount}\n"
    "Новая средняя цена: {avg_price:.2f}\n"
    "Общее количество: {total_amount:.2f}\n"
    "Общая стоимость: {total_cost:.2f}"
)

AVG_PRICE_INFO: str = (
    "🪙 Актив: {asset}\n"
    "Средняя цена: {avg_price:.2f}\n"
    "Общее количество: {total_amount:.2f}\n"
    "Общая стоимость: {total_cost:.2f}\n"
)

SELECT_ASSET: str = "Выберите актив"

SELECT_PURCHASE: str = "Выберите покупку для удаления"

PURCHASE_INFO: str = "Покупка {index}: Цена {price}, Количество {amount}"

CONFIRM_ACTION: str = "Подтвердить операцию?"

DELETED_PURCHASE: str = "Покупка удалена. Данные обновлены!"

NO_PURCHASES: str = "У вас нет покупок"

NO_PURCHASES_FOR_ASSET: str = "Нет покупок для этого актива"

NO_PURCHASES_TO_DELETE: str = "У вас нет покупок для удаления"

NO_PURCHASES_TO_CLEAR: str = "У вас нет покупок для очистки"

NO_DATA_TO_EXPORT: str = "У вас нет данных для экспорта"

DATA_CLEARED: str = "Все данные о покупках очищены!"

SUPPORTED_CRYPTOS: str = "Поддерживаемые криптовалюты:\n{currencies}"

CRYPTO_ITEM: str = "{index}. {name} ({ticker})"

ACTION_CANCELLED: str = "Операция отменена!"
