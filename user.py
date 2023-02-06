from rate_utils import get_words, rate_recognition, get_rate
from api_scripts.event_utils import main_response
from numpy import count_nonzero
from pickle import dump, load
from constants import users_file, keyboards_path
import collections_utils as coll
import random

# Загружаем словарь, с которым будет работать приложение
words = get_words()
# Словарь для хранения данных о пользователях
users = {}


# Функция для сохранения словаря пользователей в файл
def dump_users():
    global users
    with open(users_file, 'wb') as file:
        dump(users, file)


# Функция для загрузки словаря пользователей из файла
def load_users():
    global users
    try:
        with open(users_file, 'rb') as file:
            users = load(file)
    except FileNotFoundError:
        print('Users dump not found, creating new one')
        dump_users()


# Функция для создания нового пользователя
def new_user(user_id):
    global users
    if user_id in users:
        return
    users[user_id] = {
        'words': words,
        'passed_words': dict.fromkeys(words, 0.0),      # Словарь для хранения оценок пользователя для каждого слова
        'skip_words': [],                               # Список пропущенных слов
        'rating': 0.0,                                  # Средняя оценка пользователя
        'attempts_done': 0,                             # Количество попыток произнесения слова
        'response': main_response,                      # Функция ответа на сообщение
        'keyboard': f'{keyboards_path}keyboard.json',   # Текущая клавиатура пользователя
        'collection': 'Главная'}                        # Подборка слов, с которым будет работать пользователь
    dump_users()


# Функция для изменения ответа приложения для пользователя
def set_user_collection(user_id, collection_name):
    if collection_name in coll.collections:
        collection = coll.get_collection(collection_name)
    else:
        collection = coll.load_user_collection(user_id, collection_name)
    if len(collection) > 0:
        users[user_id]['words'] = collection
        users[user_id]['collection'] = collection_name


def get_user_collection(user_id):
    return users[user_id]['collection']


# Функция для изменения ответа приложения для пользователя
def set_user_response(user_id, response, keyboard):
    users[user_id]['response'] = response
    users[user_id]['keyboard'] = keyboard


# Функция для пересчета средней оценки пользователя и пересортировки словаря пользователей
def reinit_user(user_id):
    global users
    # users[user_id]['words'] = {k: v for k, v in sorted(users[user_id]['words'].items(),
    #                                                   key=lambda item: users[user_id]['words'].get(item[0]))}
    users[user_id]['rating'] = round(sum(list(users[user_id]['passed_words'].values())), 1)
    users = {k: v for k, v in sorted(users.items(),
                                     key=lambda item: users[item[0]].get('rating'), reverse=True)}
    dump_users()


# Функция для получения средней оценки слов пользователя, количества произнесенных слов и позиции пользователя в словаре
def get_user_rating(user_id):
    global users
    reinit_user(user_id)
    user_index = list(users.keys()).index(user_id)
    word_count = count_nonzero(list(users[user_id]['passed_words'].values()))
    return users[user_id]['rating'], word_count, user_index


# Функция для получения следующего слова, которое должен произнести пользователь
def get_user_word(user_id):
    word = users[user_id]['words'][0].lower()
    #word = word[0].upper() + word[1:]
    print(f'get_user_word = {word}')
    return word
    # for word in list(users[user_id]['words'].keys()):
    #    if word not in users[user_id]['skip_words']:
    #        return word


# Функция для очистки списка пропущенных слов
def clear_skiplist(user_id):
    users[user_id]['skip_words'] = []


# Функция для оценки произнесения слова пользователем
def rate_word(rec_data, user_id):
    word = get_user_word(user_id)
    if not rec_data:
        # Если пользователь не произнёс слово, то присваиваем ему случайную оценку
        rate = round(random.uniform(0.0, 0.2), 2)
        # Добавляем перед каждой буквой знак ошибки
        text_errors = ' &#10060;'.join([letter for letter in word])
    else:
        # Иначе получаем оценку и ошибки из распознавания произнесения
        rate, text_errors = rate_recognition(rec_data, word)

    text = get_rate(rate, users[user_id]['attempts_done'])  # Получаем текст для ответа приложения
    text += '\n' + text_errors  # Добавляем ошибки в текст ответа приложения
    users[user_id]['passed_words'][word] = rate  # Записываем оценку в словарь пользователя

    # Если пользователь произнёс слово правильно, пропускаем его
    if rate >= 0.2:
        users[user_id]['attempts_done'] = 0
        users[user_id]['words'].append(0)
        users[user_id]['words'] = users[user_id]['words'][1:]
        # users[user_id]['skip_words'].append(word)
        return text

    users[user_id]['attempts_done'] += 1  # Если произнесение слова неверно, увеличиваем счётчик попыток
    if users[user_id]['attempts_done'] > 1:  # Если попыток больше 2, то пропускаем слово
        users[user_id]['attempts_done'] = 0
        # users[user_id]['skip_words'].append(word)
        users[user_id]['words'].append(0)
        users[user_id]['words'] = users[user_id]['words'][1:]
    users[user_id]['passed_words'][word] = rate  # Записываем оценку в словарь пользователя
    reinit_user(user_id)  # Пересчитываем среднюю оценку пользователя и пересортировываем словарь пользователей
    return text  # Возвращаем ответ приложения


# Загружаем словарь пользователей
load_users()
