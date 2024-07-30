import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Вставьте ваш токен сюда
TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Рассчитать", "Информация"]
    keyboard.add(*buttons)
    await message.reply("Привет! Я бот, помогающий твоему здоровью. Выберите действие:", reply_markup=keyboard)


@dp.message_handler(Text(equals='Рассчитать', ignore_case=True), state="*")
async def main_menu(message: types.Message):
    inline_keyboard = InlineKeyboardMarkup()
    inline_buttons = [
        InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
        InlineKeyboardButton("Формулы расчёта", callback_data='formulas')
    ]
    inline_keyboard.add(*inline_buttons)
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(equals='calories'))
async def set_age(call: types.CallbackQuery):
    await call.message.reply("Введите свой возраст:")
    await UserState.age.set()


@dp.callback_query_handler(Text(equals='formulas'))
async def get_formulas(call: types.CallbackQuery):
    formula_text = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст + 5\n"
        "Для женщин: 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст - 161"
    )
    await call.message.reply(formula_text)


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.reply("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Используем формулу Миффлина-Сан Жеора для женщин:
    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.reply(f"Ваша норма калорий: {calories} ккал/день.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
