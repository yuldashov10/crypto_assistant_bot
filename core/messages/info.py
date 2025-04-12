WELCOME: str = (
    "Привет, {name}! 👋\n"
    "Я помогу отслеживать Ваши крипто-покупки 📊\n\n"
    "/help – Узнайте больше о боте"
)

HELP: str = (
    "📋 Команды бота:\n\n"
    "/start – Начать работу с ботом\n"
    "/add – Добавить новую покупку "
    "\n\t- выберите актив\n\t- укажите цену покупки\n\t- количество монет\n"
    "/view – Показать статистику по Вашим покупкам\n"
    "/delete – Удалить покупку"
    "\n\t- выберите актив\n\t- конкретную покупку\n"
    "/clear – Очистить все данные\n"
    "/list – Показать список поддерживаемых криптовалют\n"
    "/export – Экспортировать Ваши покупки в CSV-файл\n\n"
    "💡 Используйте /add, чтобы начать добавлять покупки!"
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
