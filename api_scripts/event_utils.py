import user
from api_scripts.message_utils import send, send_word, send_rating, send_help, send_user_collection, handle_audio
from constants import admin_id, keyboards_path, begin_text
import re


# Словарь, содержащий адреса клавиатур пользователя
keyboards = {'main': f'{keyboards_path}keyboard.json',
             'collection': f'{keyboards_path}key_collections.json',
             'create_collection': f'{keyboards_path}key_create_c.json'}

# Словарь подборок, которые создаются в данный момент
creating_collections = {}


# Основная функция ответа бота на сообщения
def main_response(user_id, text, word_count):
    print('main response')
    # Если количество введенных слов кратно 10, то отправляем рейтинг
    if word_count % 20 == 0 and word_count > 0:
        send(user_id, f'Вы прошли уже {word_count} слов! Отличный результат!')
        send_rating(user_id)
    if text == 'начать':
        send_word(user_id, begin=begin_text)
    elif text == 'хватит':
        send(user_id, 'Хорошо! Когда захочешь продолжить, напиши "начать"')
        user.clear_skiplist(user_id)
    elif text == 'рейтинг':
        send_rating(user_id)
    elif text == 'подборка':
        collection = user.get_user_collection(user_id)
        collection = collection[0].upper() + collection[1:]
        collection_word_count = len(user.users[user_id]['words'])
        user.set_user_response(user_id, collection_response, keyboards['collection'])
        message = f'Сейчас выбрана подборка "{collection}", количество слов: {collection_word_count}.' + \
                  ' Список основых подборок можно посмотреть здесь: vk.com/@enthought-podborki' + \
                  ' \nЧтобы создать новую подборку, напишите "создать".' + \
                  f'\n{user.coll.get_formatted_collections(user_id)}'
        send(user_id, message)
    elif text == 'admin':
        if str(user_id) == admin_id:
            send(user_id, '-- Режим администратора --')
            user.set_user_response(user_id, admin_response, keyboards['main'])
    else:
        send_help(user_id)


# Функция для ответа на сообщение в режиме администратора
def admin_response(user_id, text, word_count):
    if text == 'создать подборку':
        user.set_user_response(user_id, create_general_collection, keyboards['create_collection'])
        send(user_id, 'Напишите название и содержание подборки')
    elif text == 'назад':
        user.set_user_response(user_id, main_response, keyboards['main'])
        send_user_collection(user_id)


# Функция ответа при выборе коллекции
def collection_response(user_id, text, word_count):
    if text == 'создать':
        user.set_user_response(user_id, set_collection_name, keyboards['create_collection'])
        send(user_id, 'Придумайте и напишите название для вашей подборки')
    elif text == 'назад':
        user.set_user_response(user_id, main_response, keyboards['main'])
        send_user_collection(user_id)
    else:
        user.set_user_collection(user_id, text)
        user.set_user_response(user_id, main_response, keyboards['main'])
        send_user_collection(user_id)


# Функция записи имени подборки
def set_collection_name(user_id, text, word_count):
    if text == 'назад' or not text:
        user.set_user_response(user_id, main_response, keyboards['main'])
    creating_collections[str(user_id)] = text.lower()
    user.set_user_response(user_id, create_collection, keyboards['create_collection'])
    send(user_id, 'Перечислите все слова для вашей подборки через запятую')


# Функция создания пользовательской подборки
def create_collection(user_id, text, word_count):
    if text == 'назад':
        user.set_user_response(user_id, main_response, keyboards['main'])
        creating_collections[str(user_id)] = ''
    collection = re.split('\W+', text)
    collection_name = creating_collections[str(user_id)]
    user.coll.save_user_collection(user_id, collection, collection_name)
    user.set_user_collection(user_id, collection_name)
    user.set_user_response(user_id, main_response, keyboards['main'])
    send(user_id, f'Подборка "{collection_name}" из {len(collection)} слов создана успешно!')


# Функция создания основной подборки
def create_general_collection(user_id, text, word_count):
    collection = re.split('\W+', text)
    collection_name = collection[0]
    collection_name.replace('_', ' ')
    collection = collection[1:]
    user.coll.add_collection(collection_name, collection)
    user.set_user_response(user_id, admin_response, keyboards['main'])
    send(user_id, f'Подборка "{collection_name}" из {len(collection)} слов создана успешно!')


# Функция возвращает текущую функцию ответа для пользователя
def get_user_response(user_id):
    return user.users[user_id]['response']


# Основная функция для обработки всех сообщений
def handle_message(event):
    user_id = event.user_id
    # Добавляем пользователя в базу данных, если его там нет
    user.new_user(user_id)
    response = get_user_response(user_id)
    text = event.text.lower()
    _, word_count, _ = user.get_user_rating(user_id)

    # Если сообщение не текстовое, то обрабатываем аудио
    if not text:
        rec_data = handle_audio(event)
        #send(user_id, user.rate_word(rec_data, user_id))
        send_word(user_id, begin=user.rate_word(rec_data, user_id))
    else:
        # Вызываем текущую функцию ответа для пользователя
        response(user_id, text, word_count)
