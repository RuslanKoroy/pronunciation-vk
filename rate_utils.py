from colorama import init, Fore, Back, Style
from constants import words_file


# Функция для чтения слов из файла
def get_words():
    # Открываем файл с именем words_file
    with open(words_file) as file:
        words = file.readlines()
    # Удаляем перенос строки из каждого слова
    words = [word.replace('\n', '') for word in words]
    return words


# Функция для поиска ошибок в слове
def find_errors(rec_word, word):
    # Переводим слова в верхний регистр
    rec_word, word = rec_word.upper(), word.upper()
    result = ''
    # Перебираем буквы в слове
    for index, letter in enumerate(word):
        # Если распознанное слово короче, чем исходное
        if len(rec_word) <= index:
            result += f'&#10060;{letter} '
            continue
        # Если буква совпадает
        if letter == rec_word[index]:
            result += f'&#9989;{letter} '
        else:
            result += f'&#10060;{letter} '
    return result


# Функция для расчета результата распознавания
def rate_recognition(rec_data, word):
    # Берем распознанное слово
    rec_word = str(rec_data['alternative'][0]['transcript'])
    # Берем только первое слово из распознанного текста
    rec_word = rec_word.split(' ')[0].lower()
    print(f'Распознано: {rec_word}')
    # Если распознанное слово не совпадает с исходным
    if word != rec_word:
        return float(0), find_errors(rec_word, word)
    rate = float(rec_data['alternative'][0]['confidence'])
    return rate, ''


# Функция для вывода результата
def print_rate(rate):
    if rate < 0.2:
        print(Back.RED + 'Не правильно')
    else:
        if rate > 0.8:
            print(Back.GREEN + 'Отлично!')
        else:
            print(Back.YELLOW + 'Хорошо')

    print(f'Баллов: {int(rate * 100)} из 100')
    print(Style.RESET_ALL)


# Функция для получения результата
def get_rate(rate, attempts=0):
    if rate < 0.15:
        if attempts > 0:
            text = '&#9888; Не правильно'
        else:
            text = '&#9888; Не правильно, попробуйте еще раз'
    else:
        if rate > 0.8:
            text = '&#10024; Отлично!'
        else:
            text = '&#10004; Хорошо'

    text = text + f'\nБаллов: {int(rate * 100)} из 100'
    return text
