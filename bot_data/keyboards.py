from aiogram import types


def start_command_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Добавить бизнес партнера"))
    keyboard.add(types.KeyboardButton(text="Отобразить бизнес партнеров"))
    keyboard.add(types.KeyboardButton(text="Добавить представителя"))
    return keyboard


def to_menu_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Вернуться в меню"))
    return keyboard


def yes_or_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Да"))
    keyboard.add(types.KeyboardButton(text="Вернуться в меню"))
    return keyboard


def partners_btns(cb_key, data):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for i in data:
        keyboard.add(types.InlineKeyboardButton(i, callback_data=f"{cb_key}_{i}"))
    return keyboard


def order_menu_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Сделать заказ"))
    keyboard.add(types.KeyboardButton(text="Управление заказами"))
    keyboard.add(types.KeyboardButton(text="Вернуться в меню"))
    return keyboard


def to_order_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Вернуться в меню"))
    return keyboard


def add_items_to_order():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Да"))
    keyboard.add(types.KeyboardButton(text="Нет"))
    return keyboard


def partners_list_btns(data):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for i in data:
        keyboard.add(types.InlineKeyboardButton(i, callback_data=f"prt_mmb_{i}"))
    return keyboard


def order_final_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить заказ"))
    keyboard.add(types.KeyboardButton(text="Сохранить заказ"))
    keyboard.add(types.KeyboardButton(text="Удалить заказ"))
    return keyboard


def edit_order_btns(order_id):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton("Изменить дату оформления заказа", callback_data=f"edit_order_{order_id}"))
    keyboard.add(types.InlineKeyboardButton("Удалить заказ", callback_data=f"delete_order_{order_id}"))
    return keyboard
