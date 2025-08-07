import random
import string

#Генерация случайного email
def generate_random_email():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(10))
    return f"{username}@yandex.ru"

#Генерация случайного имени
def generate_random_name():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(8))

#Генерация данных для нового пользователя
def generate_user_data():
    return {
        "email": generate_random_email(),
        "password": "password",
        "name": generate_random_name()
    }