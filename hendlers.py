from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from utils import users, ATTEMPTS
from utils import get_user_info, get_random_number

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    get_user_info(message)
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )


@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    get_user_info(message)
    await message.answer(
        'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )


@user_router.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    get_user_info(message)
    user_id = message.from_user.id
    await message.answer(
        f'Всего игр сыграно: {users[user_id]["total_games"]}\n'
        f'Игр выиграно: {users[user_id]["wins"]}'
    )


@user_router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    get_user_info(message)
    user_id = message.from_user.id

    if users[user_id]['in_game']:
        users[user_id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


@user_router.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                         'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    get_user_info(message)
    user_id = message.from_user.id

    if not users[user_id]['in_game']:
        users[user_id]['in_game'] = True
        users[user_id]['secret_number'] = get_random_number()
        users[user_id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу реагировать только на '
            'числа от 1 до 100 и команды /cancel и /stat'
        )


@user_router.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    get_user_info(message)
    user_id = message.from_user.id

    if not users[user_id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


@user_router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    get_user_info(message)
    user_id = message.from_user.id

    if users[user_id]['in_game']:
        number = int(message.text)
        if number == users[user_id]['secret_number']:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            users[user_id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif number > users[user_id]['secret_number']:
            users[user_id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif number < users[user_id]['secret_number']:
            users[user_id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[user_id]['attempts'] == 0:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            await message.answer(
                'К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[user_id]["secret_number"]}\n\n'
                'Давайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@user_router.message()
async def process_other_answers(message: Message):
    get_user_info(message)
    user_id = message.from_user.id

    if users[user_id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )
