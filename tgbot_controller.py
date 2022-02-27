import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from bot_data.keyboards import *
from bot_data.db import *
from config import TOKEN
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot_data import check_registration
from browser_data import browser_controller


class Form(StatesGroup):
    members = State()
    members_login = State()
    members_pass = State()
    members_fio = State()
    members_partner = State()


class Partners(StatesGroup):
    task_type = State()


class BotUser(StatesGroup):
    current_partner = State()
    current_member = State()


class FormOrder(StatesGroup):
    order_id = State()
    item_key = State()
    count = State()
    continueAdd = State()


class DateSet(StatesGroup):
    current_date = State()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(lambda m: m.text == "Вернуться в меню", state='*')
async def back_to_menu(message, state: FSMContext):
    await state.finish()
    if message.text == "Вернуться в меню":
        await process_start_command(message)
    else:
        await order_menu(message)


@dp.callback_query_handler(lambda m: "delete_order_" in m.data)
async def delete_order_tg_bot(data):
    delete_order(int(data.data.replace("delete_order_", '')))
    await bot.send_message(data.message.chat.id, "Заказ удален!")
    await process_start_command(data.message)


@dp.message_handler(lambda m: m.text == "Управление заказами", state="*")
async def last_order_info(message, state):
    await message.answer("Меню управления заказами:", reply_markup=to_order_menu())
    data = await state.get_data()
    orders = get_all_orders(data["current_partner"], data["current_member"])
    files = os.listdir("excels/")
    for i in orders:
        current_file = ''
        for j in files:
            if f"_{i[0]}." in j:
                current_file = j
        if current_file == '':
            continue
        doc = open("excels/" + current_file, 'rb')
        if i[1] is not None:
            await message.reply_document(doc)
        else:
            await message.reply_document(doc, reply_markup=edit_order_btns(i[0]))


@dp.callback_query_handler(lambda m: "edit_order_" in m.data)
async def edit_order_date(data, state: FSMContext):
    await DateSet.current_date.set()
    await state.update_data(order_id=data.data.replace("edit_order_", ''))
    await bot.send_message(data.message.chat.id, "Отправьте дату в формате dd.mm.yyyy:")


@dp.message_handler(state=DateSet.current_date)
async def edit_order_date2(message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    set_date(int(data["order_id"]), message.text)
    await bot.send_message(message.chat.id, "Новая дата установлена!")
    await process_start_command(message)



@dp.callback_query_handler(lambda m: "members" in m.data)
async def members_cb(data, state: FSMContext):
    await bot.send_message(data.message.chat.id,
                           f"Вы хотите добавить представителя к бизнес партнеру {data.data.replace('members_', '')}?",
                           reply_markup=yes_or_menu())
    await Form.members.set()
    await state.update_data(members_partner=data.data.replace('members_', ''))


async def order_menu(message):
    await bot.send_message(message.chat.id, "Выберите нужный пункт меню заказов:", reply_markup=order_menu_btns())


@dp.callback_query_handler(lambda m: "partners" in m.data)
async def members_cb(data, state: FSMContext):
    if not is_partner_has_member(data.data):
        await bot.send_message(data.message.chat.id, "Доступ запрещен!\nУ данного бизнес партнера нет представителя!")
        await process_start_command(data.message)
    else:
        await state.update_data(current_partner=data.data.replace("partners_", ''))
        await bot.send_message(data.message.chat.id, "Выберите партнера:", reply_markup=partners_list_btns(get_members_list_from_partner(data.data.replace("partners_", ''))))


@dp.callback_query_handler(lambda m: "prt_mmb" in m.data)
async def partners_members_cb(data, state: FSMContext):
    await state.update_data(current_member=data.data.replace("prt_mmb_", ''))
    await order_menu(data.message)


# часть реализующая кнопку сделать заказ
@dp.message_handler(lambda m: m.text == "Сделать заказ")
async def make_order_1(message):
    await message.answer(f"Введите код товара:", reply_markup=to_order_menu())
    await FormOrder.item_key.set()


@dp.message_handler(state=FormOrder.item_key)
async def make_order_2(message, state: FSMContext):
    await state.update_data(item_key=message.text)
    await message.answer(f"Введите количество:", reply_markup=to_order_menu())
    await FormOrder.count.set()


@dp.message_handler(state=FormOrder.count)
async def make_order_3(message, state: FSMContext):
    data = await state.get_data()
    if "order_id" not in data.keys():
        print(data)
        current_order = create_order(data["current_partner"], data["item_key"], message.text, data["current_member"])
        await state.update_data(order_id=current_order)
    else:
        add_info_to_order(data['order_id'], data["current_partner"], data["item_key"], message.text)
    await FormOrder.continueAdd.set()
    await message.answer("Заказ сохранен.\nЖелаете добавить товары в данный заказ?", reply_markup=add_items_to_order())


@dp.message_handler(lambda m: m.text == "Удалить заказ" or m.text == "Сохранить заказ" or m.text == "Отправить заказ", state=FormOrder.continueAdd)
async def order_control(message, state: FSMContext):
    if message.text == "Удалить заказ":
        data = await state.get_data()
        id = data["order_id"]
        delete_order(id)
        await state.finish()
        await message.answer("Удалено!\nПеренаправляю в меню...")
        await process_start_command(message)
    elif message.text == "Сохранить заказ":
        await message.answer("Заказ сохранен!\nПеренаправляю в меню...")
        await state.finish()
        await process_start_command(message)
    else:
        data = await state.get_data()
        order_db = eval(get_order_by_id(data["order_id"])[2])
        items = []
        for i in order_db.keys():
            items.append([i, order_db[i]])
        d = select_logpas_by_partner(data['current_partner'])
        message.answer("Создаю заказ... Примерное время ожидания: 1.5 минуты.")
        report_addr = browser_controller.order("", d[0], d[1], items, data["order_id"], False) # -> True
        update_order_status(data["order_id"])
        doc = open(report_addr, 'rb')
        await message.answer("Данные по заказу:")
        await message.reply_document(doc)
        await message.answer("Заказ успешно отправлен!")
        await state.finish()
        await process_start_command(message)

@dp.message_handler(state=FormOrder.continueAdd)
async def make_order_4(message, state: FSMContext):
    if message.text == 'Да':
        await make_order_1(message)
    else:
        data = await state.get_data()
        order_db = eval(get_order_by_id(data["order_id"])[2])
        items = []
        for i in order_db.keys():
            items.append([i, order_db[i]])
        d = select_logpas_by_partner(data['current_partner'])
        await message.answer("Хорошо. Проверяю данные... (обычно это занимает 1.5 минуты)", reply_markup=to_order_menu())
        report_addr = browser_controller.order("", d[0], d[1], items, data["order_id"], False)
        doc = open(report_addr, 'rb')
        await message.answer("Предварительные данные по заказу:", reply_markup=order_final_btn())
        await message.reply_document(doc)


# часть реализующая кнопку сделать заказ


@dp.message_handler(state=Form.members)
async def members_yes(message):
    await message.answer("Введите логин:", reply_markup=to_menu_btn())
    await Form.members_login.set()


@dp.message_handler(state=Form.members_login)
async def members_login(message, state: FSMContext):
    await message.answer("Введите пароль:", reply_markup=to_menu_btn())
    await Form.members_pass.set()
    await state.update_data(members_login=message.text)


@dp.message_handler(state=Form.members_pass)
async def members_fio(message, state: FSMContext):
    await message.answer("Введите ФИО представителя:", reply_markup=to_menu_btn())
    await Form.members_fio.set()
    await state.update_data(members_pass=message.text)


@dp.message_handler(state=Form.members_fio)
async def members_check(message, state: FSMContext):
    await state.update_data(members_fio=message.text)
    await message.answer("Подождите 10 секунд. Производится проверка введенных данных.", reply_markup=to_menu_btn())
    data = await state.get_data()
    if check_registration.main(data["members_login"], data["members_pass"]):
        write_member(data)
        await message.answer("Данные прошли проверку!\nСохранено.")
    else:
        await message.answer("Данные не валидны!\nДобавление не будет произведено.")
    await state.finish()
    await process_start_command(message)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Здравствуйте.\n\nВыберите нужный пункт меню", reply_markup=start_command_btn())


@dp.message_handler(lambda m: m.text == "Добавить бизнес партнера")
async def add_bp_start(message: types.Message):
    await message.reply("Введите ФИО партнера:", reply_markup=to_menu_btn())
    await Partners.task_type.set()


@dp.message_handler(state=Partners.task_type)
async def add_bp_finish(message: types.Message, state: FSMContext):
    await state.finish()
    write_partner(message.text)
    await message.reply(f"Партнер {message.text} добавлен!\nПеренаправляю в меню...")
    await process_start_command(message)


@dp.message_handler(lambda m: m.text == "Отобразить бизнес партнеров")
async def partners(message):
    await message.answer("Выберите партнера:", reply_markup=partners_btns("partners", get_partners_list()))


@dp.message_handler(lambda m: m.text == "Добавить представителя")
async def members(message):
    await message.answer("К какому бинес партнеру прикрепить представителя:",
                         reply_markup=partners_btns("members", get_partners_list()))



if __name__ == '__main__':
    executor.start_polling(dp)
