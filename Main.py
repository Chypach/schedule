import CFG
import asyncio
from typing import Optional
import logging
import SQL
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, labeled_price, pre_checkout_query, PreCheckoutQuery, LabeledPrice
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import tracemalloc
import Schedule_1W_1_group
import Schedule_1W_2_group
import Schedule_2W_1_group
import Schedule_2W_2_group
# Включить отслеживание распределения памяти
tracemalloc.start()

# Установите ограничение на количество кадров в трассировке (опционально)
tracemalloc.START_FRAMES_COUNT = 10
# ----------------------------------------------------------------------------
#
#                     ╔══╗╔══╗╔╗╔╗╔═══╗╔══╗─╔╗╔╗╔╗──╔═══╗
#                     ║╔═╝║╔═╝║║║║║╔══╝║╔╗╚╗║║║║║║──║╔══╝
#                     ║╚═╗║║──║╚╝║║╚══╗║║╚╗║║║║║║║──║╚══╗
#                     ╚═╗║║║──║╔╗║║╔══╝║║─║║║║║║║║──║╔══╝
#                     ╔═╝║║╚═╗║║║║║╚══╗║╚═╝║║╚╝║║╚═╗║╚══╗
#                     ╚══╝╚══╝╚╝╚╝╚═══╝╚═══╝╚══╝╚══╝╚═══╝
#                                                  Created By student SE102
# ----------------------------------------------------------------------------


# + добавить БД
#НУЖНО ДОБАВИТЬ ОЖИДАНИЕ ОТВЕТА!!!!
# смену недели
# 1-я или 2-я группа англа



logging.basicConfig(level=logging.INFO) # Включаем логирование, чтобы не пропустить важные сообщения
bot = Bot(CFG.BOT_TOKEN) # Объект бота
dp = Dispatcher() # Диспетчер

class NumbersCallbackFactory(CallbackData, prefix="f"):
    action: str
    user_ID: Optional[int] = None
    chat_ID: Optional[int] = None
    message_ID: Optional[int] = None
    time: Optional[str] = None

bot.send_message
@dp.message(Command("start"))
async def cmd_start(message: types.Message,
                    state: FSMContext):
    await state.clear()



    user_ID = message.from_user.id


    builder = InlineKeyboardBuilder()
    builder.button(
        text="Далее", callback_data=NumbersCallbackFactory(action="Next_step", user_ID=user_ID)
    )

    # инлайн кнопка проверить подписку

    await message.answer("""
    Я бот расписания ПрИ 102, хули глаза вылупил?
        """, reply_markup=builder.as_markup())

@dp.message(F.text.lower() == "меню")
async def menu(message: types.Message, state: FSMContext):
    await state.clear()


    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить время", callback_data=NumbersCallbackFactory(action="update_time")
    )
    builder.button(
        text="Посмтреть рассписание", callback_data=NumbersCallbackFactory(action="check_schedule")
    )


    await bot.send_message(message.chat.id, """Меню""",reply_markup=builder.as_markup())
    await bot.send_message(message.chat.id, f"{Schedule_1W_1_group.Monday_1()}")

@dp.callback_query(NumbersCallbackFactory.filter(F.action == "check_schedule"))
async def check_schedule(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    None


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "Next_step"))
async def Next_step(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):

    user_ID = callback.from_user.id

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да", callback_data=NumbersCallbackFactory(action="Yea", user_ID=user_ID)
    )

    builder.button(
        text="Нет", callback_data=NumbersCallbackFactory(action="No", user_ID=user_ID)
    )

    await callback.message.edit_text("""Так, давай разберемся кое в чём.
Я могу присылать тебе сообщение с расписанием автоматически в выбранное тобой время.
     
В независимости от твоего выбора ты всегда сам можешь изменить время отправки расписания и ПОСМОТРЕТЬ ЕГО САМ.

Хочешь чтобы я сам присылал тебе уведомление?""", reply_markup = builder.as_markup())
    await callback.answer()


class Form(StatesGroup):
    waiting_for_time = State()
    waiting_for_Number = State()
    waiting_for_update_time = State()


# НУЖНО ДОБАВИТЬ ОЖИДАНИЕ ОТВЕТА!!!!
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "Yea"))
async def Yea(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    user_ID = callback.from_user.id

    await state.set_state(Form.waiting_for_time)
    await callback.message.edit_text("""Отлично! введи время, в которое мне присылать тебе расписание, в 24-х формате ЧЧ:ММ.
Например 20:31""")


# принимаем текст
@dp.message(Form.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    time = str(message.text.strip())
    if CFG.is_valid_time(time) == True:
        await bot.send_message(message.chat.id ,"Отлично, почти закончили! Введи номер своей группы по англискому")
        await state.clear()
        await state.update_data(user_time=time)
        await state.set_state(Form.waiting_for_Number)


    else:
        print(False)


@dp.message(Form.waiting_for_Number)
async def process_time(message: types.Message, state: FSMContext):
    group = message.text.strip()

    kb = [
        [types.KeyboardButton(text="Меню")],
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)


    data = await state.get_data()
    time = data.get('user_time')
    await bot.send_message(message.chat.id, "записал тебя в списочек  ̶п̶и̶д̶о̶р̶а̶с̶о̶в̶, но пока только карандашом", reply_markup=keyboard)
    SQL.add_user(message.chat.id, time, group)



@dp.callback_query(NumbersCallbackFactory.filter(F.action == "No"))
async def No(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    kb = [
        [types.KeyboardButton(text="Меню")],
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)


    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(callback.message.chat.id,"""Окей, тогда просто введи 'меню', если захочешь чтоб я присылал тебе время""",
                                     reply_markup=keyboard)


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "update_time"))
async def update_time(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    await state.set_state(Form.waiting_for_update_time)
    await bot.send_message(callback.message.chat.id,"""Введи время, в которое мне присылать тебе расписание, в 24-х формате ЧЧ:ММ.
Например 20:31""")


@dp.message(Form.waiting_for_update_time)
async def process_time(message: types.Message, state: FSMContext):
    time = str(message.text.strip())
    if CFG.is_valid_time(time) == True:
        await bot.send_message(message.chat.id ,"Обновил время отправки")
        await state.clear()
        SQL.update_time(message.chat.id, time)


    else:
        print(False)




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())