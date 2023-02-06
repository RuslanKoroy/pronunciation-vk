#!/usr/bin/python
# -*- coding: utf-8 -*-

# Импортируем необходимые библиотеки
import vk_api
from vk_api.longpoll import VkLongPoll, VkLongpollMode, VkEventType

# Импортируем функции из других файлов
import user
from api_scripts.message_utils import set_vk
from api_scripts.event_utils import handle_message
from constants import vk_api_token

# Авторизуемся в vk
vk_session = vk_api.VkApi(token=vk_api_token)
vk = vk_session.get_api()
set_vk(vk)

# Создаем экземпляр longpoll
VkLongpollMode(2)
longpoll = VkLongPoll(vk_session)
print("Скрипт запущен")


# Функция для получения сообщений
def catch_events():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                handle_message(event)


def loop_listen():
    while True:
        try:
            catch_events()
        except KeyboardInterrupt:
            print(' - KeyboardInterrupt - ')
            break
        except Exception as exception:
            print('Error:', exception)
            continue
