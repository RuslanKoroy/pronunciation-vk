help_file = 'help.txt'
users_file = 'users.pkl'
words_file = 'words.txt'
audio_path = './words_audio/'
collections_path = './collections/'
keyboards_path = './api_scripts/'

admin_id = ''
vk_api_token = ''
begin_text = 'Отлично, начнем! Я пришлю слово и пример произношения, а вы запишите голосовое сообщение с произношением'
default_text = 'Напишите "начать", чтобы начать тренировку, или "помощь", чтобы просмотреть команды'


def rating_text(rating, word_count, user_index):
    return f'&#11088; Ваш рейтинг: {str(rating)}\n&#128215;' + \
           f' Слов пройдено: {str(word_count)}\n&#128081; ' + \
           f' Место в рейтинге: {user_index+1}\n\nЕсли вам нравится наш бот, расскажите о нас друзьям!'
