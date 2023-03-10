Сервис для практики произношения английских слов через бота ВКонтакте
============================================

Сервис для тренировки произношения английских слов, использует Google Speech Recognition для оценки произношения по голосовому сообщению произношения слова. Пользователи могут выбрать или создать подборку слов, которые они хотят практиковать, и получать информацию о качестве своего произношения. 

Сервис предоставляет пользователям статистику по произношению и дает примеры произношения слов, чтобы помочь им улучшить произношение. Также пользователи могут слушать правильное произношение слов и прослушивать свои записи, чтобы сравнить свое произношение с правильным.

# Установка

## Python

Для работы бота необходимо установить [Python версии 3.10 и выше](https://www.python.org/downloads/).

## Установка необходимых пакетов

Список пакетов перечислен в файле `requirements.txt`. Для установки запустите pip:

    python3 -m pip install -r requirements.txt

# Использование

## Запуск

### Способ 1

Замените в файле constants.py значения vk_api_token на значение [токена вашего сообщества ВКонтакте](https://vk.com/dev/bots_docs?f=1.1.%20%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0) и admin_id на ID вашей страницы ВКонтакте. Запустите скрипт main.py.

### Способ 2

Запустите скрипт main.py, в аргументах укажите значение токена вашего сообщества ВКонтакте и ID вашей страницы ВКонтакте. 

    python3 main.py --token <token сообщества> --admin_id <ваш id>

Для запуска в режиме отладки добавьте аргумент `--test True`.

### Список команд бота

- Начать - запустить тренировку
- Рейтинг - просмотреть свой рейтинг
- Подборка - выбрать или создать пользовательскую подборку
- Помощь - просмотреть список команд
- Admin - режим администратора (работает только для указанной в admin_id страницы)
- Создать подборку - создать основную подборку (в режиме администратора)

Пример использования бота:

![][1]

[1]: example.jpg