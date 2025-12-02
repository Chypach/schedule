import CFG
import asyncio
from typing import Optional
import logging
import SQL
from aiogram.types import Message, labeled_price, pre_checkout_query, PreCheckoutQuery, LabeledPrice, \
    InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import tracemalloc

import TEST
import TTime
from EvenOddWeek import NomOfWeek

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
# НУЖНО ДОБАВИТЬ ОЖИДАНИЕ ОТВЕТА!!!!
# смену недели
# 1-я или 2-я группа англа


logging.basicConfig(level=logging.INFO)  # Включаем логирование, чтобы не пропустить важные сообщения
bot = Bot(CFG.BOT_TOKEN)  # Объект бота
dp = Dispatcher()  # Диспетчер


class NumbersCallbackFactory(CallbackData, prefix="f"):
    action: str
    user_ID: Optional[int] = None
    chat_ID: Optional[int] = None
    message_ID: Optional[int] = None
    time: Optional[str] = None



@dp.message(Command("start"))
async def cmd_start(message: types.Message,
                    state: FSMContext):
    await state.clear()

    user_ID = message.from_user.id

    try:
        if SQL.search_lang(user_ID) == "RU":
            builder = InlineKeyboardBuilder()
            builder.button(
                text="Выбрать группу", callback_data=NumbersCallbackFactory(action="Next_step", user_ID=user_ID)
            )
            await message.answer("""
                Привет! Я бот расписания ПрИ-102. Я высылаю расписание по кнопке. Давай выберем твою группу английского.
                    """, reply_markup=builder.as_markup())
        elif SQL.search_lang(user_ID) == "EN":

            builder = InlineKeyboardBuilder()
            builder.button(
                text="Select a group", callback_data=NumbersCallbackFactory(action="EN_Next_step", user_ID=user_ID)
            )
            await message.answer("""
                            Hi! I'm the 102 PR schedule bot. I send the schedule via the button. Let's choose your English group.
                                """, reply_markup=builder.as_markup())
    except:
        SQL.add_user(user_ID, 1, "RU")

        builder = InlineKeyboardBuilder()
        builder.button(
            text="Выбрать группу", callback_data=NumbersCallbackFactory(action="Next_step", user_ID=user_ID)
        )
        await message.answer("""
                        Привет! Я бот расписания ПрИ-102. Я высылаю расписание по кнопке. Давай выберем твою группу английского.
                            """, reply_markup=builder.as_markup())


@dp.message(F.text.lower() == "расписание на сегодня")
async def Schedule1(message: types.Message, state: FSMContext):

    try:
        nomOfG = SQL.search_db(message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(message.chat.id,"Произошла ошибка и я вывел расписание для 1 группы английского. Возможно тебя нет в базе данных, пропиши /start")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek()
    day = TTime.wtoday()
    await bot.send_message(message.chat.id, f"<blockquote>{TEST.get_schedule(group, week_type, day)}</blockquote>",parse_mode="HTML")
    # await bot.send_message(message.chat.id, f"{Schedule_1W_1_group.Monday_1()}")

@dp.message(F.text.lower() == "расписание на завтра")
async def Schedule1(message: types.Message, state: FSMContext):

    try:
        nomOfG = SQL.search_db(message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(message.chat.id,"Произошла ошибка и я вывел расписание для 1 группы английского. Возможно тебя нет в базе данных, пропиши /start")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek(1)
    day = TTime.wtomorrow()
    await bot.send_message(message.chat.id, f"<blockquote>{TEST.get_schedule(group, week_type, day)}</blockquote>",parse_mode="HTML")
    # await bot.send_message(message.chat.id, f"{Schedule_1W_1_group.Monday_1()}")

@dp.message(F.text.lower() == "меню")
async def Menu(message: types.Message, state: FSMContext):

    builder = InlineKeyboardBuilder()
    builder.button(
        text="🇺🇸 English", callback_data=NumbersCallbackFactory(action="EN")
    )
    builder.button(
        text="Изменить номер группы английского", callback_data=NumbersCallbackFactory(action="Next_step")
    )
    builder.button(
        text="Расписание на всю неделю", callback_data=NumbersCallbackFactory(action="check_schedule")
    ).adjust(1)
    await bot.send_message(message.chat.id, """
    <pre><code class="МЕНЮ">
            МЕНЮ
        Тут ты можешь:
- Выбрать английский язык

- Изменить номер группы английского

- Посмотреть расписание на всю неделю</code></pre>
        """, reply_markup=builder.as_markup(),parse_mode="HTML")




@dp.callback_query(NumbersCallbackFactory.filter(F.action == "check_schedule"))
async def check_schedule(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):

    try:
        nomOfG = SQL.search_db(callback.message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(callback.message.chat.id,"Произошла ошибка и я вывел расписание для 1 группы английского. Возможно тебя нет в базе данных, пропиши /start")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek()
    await bot.send_message(callback.message.chat.id, f"""
<blockquote expandable>Понедельник
{TEST.get_schedule(group,week_type,"monday")}
</blockquote>
<blockquote expandable>Вторник
{TEST.get_schedule(group,week_type,"tuesday")}
</blockquote>
<blockquote expandable>Среда
{TEST.get_schedule(group,week_type,"wednesday")}
</blockquote>
<blockquote expandable>Четверг
{TEST.get_schedule(group,week_type,"thursday")}
</blockquote>
<blockquote expandable>Пятница
{TEST.get_schedule(group,week_type,"friday")}
</blockquote>
<blockquote expandable>Суббота
{TEST.get_schedule(group,week_type,"saturday")}
</blockquote>
    """,parse_mode="HTML")


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "Next_step"))
async def Next_step(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    user_ID = callback.from_user.id

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Я в 1-й группе английского", callback_data=NumbersCallbackFactory(action="first", user_ID=user_ID)#тут было Yea
    )

    builder.button(
        text="Я во 2-й группе английского", callback_data=NumbersCallbackFactory(action="second", user_ID=user_ID)#тут было No
    ).adjust(1)

    await callback.message.edit_text("""В какой ты группе английского?""", reply_markup=builder.as_markup())
    await callback.answer()


# НУЖНО ДОБАВИТЬ ОЖИДАНИЕ ОТВЕТА!!!!
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "first"))
async def first(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    kb = [
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")],
        [types.KeyboardButton(text="Меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id,
                           """Отлично! Отныне я буду присылать тебе расписание с учетом твоей группы""",
                           reply_markup=keyboard)
    SQL.add_user(callback.message.chat.id, 1,"RU")


    # SQL.add_user(message.chat.id, time, group)


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "second"))    #тут надо добавить в БД ID и группу англа
async def second(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    kb = [
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")],
        [types.KeyboardButton(text="Меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id,
                           """Отлично! Отныне я буду присылать тебе расписание с учетом твоей группы""",
                           reply_markup=keyboard)
    SQL.add_user(callback.message.chat.id, 2, "RU")


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN"))
async def Change_number(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
):
    nomOG = SQL.search_db(callback.message.chat.id)
    SQL.add_user(callback.message.chat.id, nomOG, "EN")
    kb = [
        [types.KeyboardButton(text="Schedule for today")],
        [types.KeyboardButton(text="Schedule for tomorrow")],
        [types.KeyboardButton(text="Menu")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id, "Applied!", reply_markup=keyboard)



#                                   EN
#===============================================================================================
#===============================================================================================
#===============================================================================================
#===============================================================================================

@dp.message(F.text.lower() == "schedule for today")
async def Schedule1(message: types.Message, state: FSMContext):
    try:
        nomOfG = SQL.search_db(message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(message.chat.id,
                               "An error occurred and I displayed the schedule for English Group 1. You may not be in the database; try /start.")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek()
    day = TTime.wtoday()
    await bot.send_message(message.chat.id, f"<blockquote>{TEST.get_EN_schedule(group, week_type, day)}</blockquote>",parse_mode="HTML")
    # await bot.send_message(message.chat.id, f"{Schedule_1W_1_group.Monday_1()}")


@dp.message(F.text.lower() == "schedule for tomorrow")
async def Schedule1(message: types.Message, state: FSMContext):
    try:
        nomOfG = SQL.search_db(message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(message.chat.id,
                               "An error occurred and I displayed the schedule for English Group 1. You may not be in the database; type /start.")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek(1)
    day = TTime.wtomorrow()
    await bot.send_message(message.chat.id, f"<blockquote>{TEST.get_EN_schedule(group, week_type, day)}</blockquote>",parse_mode="HTML")
    # await bot.send_message(message.chat.id, f"{Schedule_1W_1_group.Monday_1()}")


@dp.message(F.text.lower() == "menu")
async def EN_Schedule1(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🇷🇺 Русский язык", callback_data=NumbersCallbackFactory(action="RU")
    )
    builder.button(
        text="Change English group number", callback_data=NumbersCallbackFactory(action="EN_Next_step")
    )
    builder.button(
        text="Schedule for the whole week", callback_data=NumbersCallbackFactory(action="EN_check_schedule")
    ).adjust(1)
    await bot.send_message(message.chat.id, """<pre><code class="МЕНЮ">
            MENU
        Here you can:
- Switch language
- Change your English group number
- View the schedule for the whole week
    """, reply_markup=builder.as_markup())


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN_Change_number"))
async def Change_number(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    None



@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN_check_schedule"))
async def check_schedule(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):

    try:
        nomOfG = SQL.search_db(callback.message.chat.id)
    except:
        nomOfG = 1
        await bot.send_message(callback.message.chat.id,"An error occurred and I displayed the schedule for English Group 1. You may not be in the database; type /start.")

    group = f"group_{nomOfG}"
    week_type = NomOfWeek()
    await bot.send_message(callback.message.chat.id, f"""
<blockquote expandable>monday
{TEST.get_EN_schedule(group,week_type,"monday")}
</blockquote>
<blockquote expandable>tuesday
{TEST.get_EN_schedule(group,week_type,"tuesday")}
</blockquote>
<blockquote expandable>wednesday
{TEST.get_EN_schedule(group,week_type,"wednesday")}
</blockquote>
<blockquote expandable>thursday
{TEST.get_EN_schedule(group,week_type,"thursday")}
</blockquote>
<blockquote expandable>friday
{TEST.get_EN_schedule(group,week_type,"friday")}
</blockquote>
<blockquote expandable>saturday
{TEST.get_EN_schedule(group,week_type,"saturday")}
</blockquote>
    """,parse_mode="HTML")


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN_Next_step"))
async def Next_step(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    user_ID = callback.from_user.id

    builder = InlineKeyboardBuilder()
    builder.button(
        text="I'm in the 1st English group.", callback_data=NumbersCallbackFactory(action="EN_first", user_ID=user_ID)
        # тут было Yea
    )

    builder.button(
        text="I'm in the 2nd English group.", callback_data=NumbersCallbackFactory(action="EN_second", user_ID=user_ID).adjust(1)
        # тут было No
    )

    await callback.message.edit_text("""What English group are you in?""", reply_markup=builder.as_markup())
    await callback.answer()


# class Form(StatesGroup):
#     waiting_for_time = State()
#     waiting_for_Number = State()
#     waiting_for_update_time = State()


# НУЖНО ДОБАВИТЬ ОЖИДАНИЕ ОТВЕТА!!!!
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN_first"))
async def first(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    kb = [
        [types.KeyboardButton(text="Schedule for today")],
        [types.KeyboardButton(text="Schedule for tomorrow")],
        [types.KeyboardButton(text="Menu")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id,
                           """Great! From now on, I'll send you a schedule tailored to your group.""",
                           reply_markup=keyboard)
    SQL.add_user(callback.message.chat.id, 1, "EN")




@dp.callback_query(NumbersCallbackFactory.filter(F.action == "EN_second"))  # тут надо добавить в БД ID и группу англа
async def second(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    SQL.add_user(callback.message.chat.id, 2, "EN")
    kb = [
        [types.KeyboardButton(text="Schedule for today")],
        [types.KeyboardButton(text="Schedule for tomorrow")],
        [types.KeyboardButton(text="Menu")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id,
                           """Great! From now on, I'll send you a schedule tailored to your group.""",
                           reply_markup=keyboard)


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "RU"))
async def Change_number(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
):
    nomOG = SQL.search_db(callback.message.chat.id)
    SQL.add_user(callback.message.chat.id, nomOG, "RU")
    kb = [
        [types.KeyboardButton(text="Расписание на сегодня")],
        [types.KeyboardButton(text="Расписание на завтра")],
        [types.KeyboardButton(text="Меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True)

    await bot.send_message(callback.message.chat.id, "Применил!", reply_markup=keyboard)


#===============================================================================================
#===============================================================================================
#===============================================================================================
#===============================================================================================
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
