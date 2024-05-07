from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import Parser
import time

router = Router()

min = 0.0
max = 0.0

sendMessages = False
limitsAreSet = False
userId = ''
def check_string(input_string, allowed_chars):
    for char in input_string:
        if char not in allowed_chars:
            return False
    return True
allowedchars = '0123456789.'
class Limits(StatesGroup):
    min = State()
    max = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    global userId
    userId = message.from_user.id
    await message.answer(f'Привет, в этом боте ты можешь установить минимальную и максимальную '
                         f'планку для курса доллара по отношению к рублю, если доллар выйдет за '
                         f'заданные рамки то бот направит тебе уведомление', reply_markup = kb.main)

@router.message(F.text == 'Вкл./Выкл. сообщения от бота')
async def changemsgsendstate(message: Message):
    global sendMessages
    if (sendMessages):
        sendMessages = False
        await message.answer('Сообщения от бота отключены')
    else:
        sendMessages = True
        await message.answer('Сообщения от бота включены')
    while(sendMessages and limitsAreSet):
        usd = Parser.parse()
        fusd = float(usd)
        if(fusd > max or fusd < min):
           await message.answer('Курс вышел за установленные рамки и равен: ' + usd)
        await asyncio.sleep(60)

@router.message(F.text == 'Задать границы курса')
async def setlimits(message: Message, state: FSMContext):
    global sendMessages
    global limitsAreSet
    sendMessages = False
    limitsAreSet = False
    await message.answer('Правило ввода границ: допускаются только цифры и точка (.)')
    await state.set_state(Limits.min)
    await message.answer('Введите минимальное значение')

@router.message(Limits.min)
async def setlimits_min(message: Message, state: FSMContext):
    if(check_string(message.text,allowedchars)):
        await state.update_data(min = message.text)
        await state.set_state(Limits.max)
        await message.answer('Введите максимальное значение')
    else:
        await state.clear()
        await message.answer('Вы ввели неверное значение, нажмите на кнопку и попробуйте снова')

@router.message(Limits.max)
async def setlimits_max(message: Message, state: FSMContext):
    global sendMessages
    global limitsAreSet
    global min
    global max
    data = await state.get_data()
    if (check_string(message.text, allowedchars) and (float(message.text) > float(str(data["min"])))):
        await state.update_data(max=message.text)
        data = await state.get_data()
        await message.answer(f'Вы успешно задали следующие лимиты:\nМинимальное значение: {data["min"]}\nМаксимальное значение: {data["max"]}')
        min = float(str(data["min"]))
        max = float(str(data["max"]))
        await state.clear()
        limitsAreSet = True
    else:
        await state.clear()
        await message.answer('Вы ввели неверное значение, нажмите на кнопку и попробуйте снова')
