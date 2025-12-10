import random

# Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}

# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

ATTEMPTS = 5