# Импортируем необходимые библиотеки
import time
import requests
import random
import os

# Импортируем функции из других файлов
from speech_utils import recognize_from_file
from api_scripts.http_utils import get_audio_file
from api_scripts.words_tts import gen_file
import user
from constants import help_file, audio_path, rating_text

vk = 0


def set_vk(gvk):
    global vk
    vk = gvk


# Функция для отправки сообщения
def send(user_id, message):
    time.sleep(1.6)
    print('send message')
    vk.messages.send(user_id=str(user_id), message=str(message), random_id=0,
                     keyboard=open(user.users[user_id]['keyboard'], "r", encoding="UTF-8").read())


# Функция для отправки слова пользователю
def send_word(user_id, begin = ''):
    word = user.get_user_word(user_id)
    send(user_id, f'{begin}\n\n&#128172; Произнесите слово "{word}"')
    
    try:
        audio_file = audio_path + word + '.ogg'
        if not os.path.isfile(audio_file):
            gen_file(word)
        send_audio_message(user_id, audio_file)
    except Exception as exception:
        print(f'Error in sending audio file: {exception}')


# Функция для отправки списка команд
def send_help(user_id):
    with open(help_file, encoding='utf8') as file:
        help_text = ''.join(file.readlines())
        send(user_id, help_text)


# Функция для отправки рейтинга
def send_rating(user_id):
    rating, word_count, user_index = user.get_user_rating(user_id)
    send(user_id, rating_text(rating, word_count, user_index))


def send_user_collection(user_id):
    collection = user.get_user_collection(user_id)
    collection = collection[0].upper() + collection[1:]
    send(user_id, f'Выбрана подборка "{collection}"')


# Функция для распознавания голосового сообщения
def handle_audio(event):
    audio_url = get_audio_url(event)
    if len(audio_url) > 0:
        audio_file = get_audio_file(audio_url)
        recognized = recognize_from_file(audio_file)
        return recognized
    return False


# Функция для получения URL голосового сообщения
def get_audio_url(event):
    audio_url = ''
    if len(event.attachments) > 0:
        if event.attachments['attach1_type'] == 'doc':
            audio_url = event.attachments['attachments']
            audio_url = audio_url[audio_url.find('link_ogg') + len('link_ogg":"'):]
            audio_url = audio_url[:audio_url.find('"')]
    return audio_url


# Функция для отправки голосового сообщения
def send_audio_message(user_id, filepath):
    # Получаем адрес для загрузки файла
    upload_url = vk.docs.getMessagesUploadServer(type="audio_message", peer_id=user_id)["upload_url"]

    # Отправляем файл на адрес загрузки
    r = requests.post(upload_url, files={
        "file": open(filepath, "rb")
    })

    # Получаем информацию о загруженном документе
    file = r.json()["file"]
    document = vk.docs.save(file=file)["audio_message"]

    # Извлекаем идентификатор документа и владельца
    owner_id = document["owner_id"]
    doc_id = document["id"]

    # Отправляем документ пользователю
    vk.messages.send(
        peer_id=user_id,
        random_id=random.randint(0, 2147483647),
        attachment=f"doc{owner_id}_{doc_id}"
    )