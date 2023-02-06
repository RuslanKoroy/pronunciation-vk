from gtts import gTTS
from constants import words_file
import os

from pydub import AudioSegment


def gen_file(word):
	language = 'en'
	myobj = gTTS(text=word, lang=language, slow=False)
	path = f'./words_audio/{word}.mp3'
	myobj.save(path)
	mp3_to_ogg(path)


def mp3_to_ogg(filepath):
	AudioSegment.from_mp3(filepath).export(f'{filepath[:-4]}.ogg', format='ogg')


def wordlist_to_file(path):
	with open(path) as file:
		words = file.readlines()
		words = [word.replace('\n', '') for word in words]

	for index, word in enumerate(words):
		gen_file(word)
		print(f'saved {index}/{len(words)}')