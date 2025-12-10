import random

from aiogram.types import Message

ATTEMPTS = 5

# Словарь, в котором будут храниться данные пользователей
users = {}

# Функция проверяющая есть ли user в словаре
def get_user_info(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }
    return users[user_id]


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

