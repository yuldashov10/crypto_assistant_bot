from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def calculate_pagination(
    total_items: int, items_per_page: int, page: int
) -> tuple[int, int, int, int]:
    """
    Вычисляет параметры пагинации.

    :return: Общее количество страниц, текущая страница, начальный индекс,
    конечный индекс.
    """
    total_pages: int = (total_items + items_per_page - 1) // items_per_page
    if total_pages == 0:
        total_pages = 1

    page: int = max(0, min(page, total_pages - 1))
    start_idx: int = page * items_per_page
    end_idx: int = min(start_idx + items_per_page, total_items)

    return total_pages, page, start_idx, end_idx


def create_item_buttons(
    items: list[str | dict[str, Any]],
    start_idx: int,
    end_idx: int,
    callback_prefix: str,
    button_text_key: str = "text",
    button_value_key: str = "value",
    buttons_per_row: int = 5,
) -> list[list[InlineKeyboardButton]]:
    """
    Создает кнопки для элементов.

    :param items: Список элементов.
    :param start_idx: Начальный индекс.
    :param end_idx: Конечный индекс.
    :param callback_prefix: Префикс для callback_data.
    :param button_text_key: Ключ для текста кнопки.
    :param button_value_key: Ключ для значения в callback_data.
    :param buttons_per_row: Количество кнопок в строке.
    :return: Список строк с кнопками.
    """
    buttons: list[list[InlineKeyboardButton]] = []
    current_row: list[InlineKeyboardButton] = []

    for idx in range(start_idx, end_idx):
        item = items[idx]
        if isinstance(item, str):
            text = item
            value = item
        else:
            text = str(item.get(button_text_key, ""))
            value = str(item.get(button_value_key, ""))

        button = InlineKeyboardButton(
            text=text, callback_data=f"{callback_prefix}:{value}"
        )
        current_row.append(button)

        if len(current_row) == buttons_per_row:
            buttons.append(current_row)
            current_row = []

    if current_row:
        buttons.append(current_row)

    return buttons


def create_navigation_buttons(
    callback_prefix: str, page: int, total_pages: int
) -> list[InlineKeyboardButton]:
    """
    Создает навигационные кнопки (Назад/Вперед).

    :return: Список навигационных кнопок.
    """
    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"{callback_prefix}:prev:{page}",
            )
        )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"{callback_prefix}:next:{page}",
            )
        )
    return nav_buttons


def create_paginated_keyboard(
    items: list[str | dict[str, Any]],
    callback_prefix: str,
    items_per_page: int = 5,
    page: int = 0,
    btn_text_key: str = "text",
    btn_value_key: str = "value",
) -> tuple[InlineKeyboardMarkup, int]:
    """
    Создает инлайн-клавиатуру с пагинацией.

    :param items: Список элементов для отображения.
    :param callback_prefix: Префикс для callback_data.
    :param items_per_page: Количество элементов на странице.
    :param page: Текущая страница.
    :param btn_text_key: Ключ для текста кнопки, если items список словарей.
    :param btn_value_key: Ключ для значения в callback_data,
    если items список словарей.
    :return: Клавиатура и общее количество страниц.
    """
    if not items:
        return InlineKeyboardMarkup(inline_keyboard=[]), 0

    total_items = len(items)
    total_pages, page, start_idx, end_idx = calculate_pagination(
        total_items, items_per_page, page
    )

    buttons = create_item_buttons(
        items,
        start_idx,
        end_idx,
        callback_prefix,
        btn_text_key,
        btn_value_key,
    )

    nav_buttons = create_navigation_buttons(
        callback_prefix,
        page,
        total_pages,
    )
    if nav_buttons:
        buttons.append(nav_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard, total_pages
