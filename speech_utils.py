import speech_recognition as sr
import soundfile as sf
from pydub import AudioSegment

r = sr.Recognizer()


# функция для преобразования файла OGG в формат WAV
def ogg_to_wav(filepath):
    wfn = filepath.replace('.ogg', '.wav')  # замена расширения файла
    x = AudioSegment.from_file(filepath)
    x.export(wfn, format='wav')  # экспорт в формат WAV
    return wfn


# функция для преобразования файла OGG в формат WAV с использованием библиотеки soundfile
def ogg_to_wav_sf(filepath):
    data, samplerate = sf.read(filepath, subtype='OGG')
    new_file = filepath[:-3] + '.wav'
    sf.write(new_file, data, samplerate)
    return new_file


# функция для распознавания речи с использованием микрофона
def listen_and_recognize():
    with sr.Microphone() as source:
        print('Слушаю...')
        audio = r.listen(source)  # чтение аудио с микрофона
    try:
        print('Распознаю...')
        result = r.recognize_google(audio, show_all=True)
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition не может понять аудио")
    except sr.RequestError as e:
        print("Не удается запросить результаты из службы Google Speech Recognition; {0}".format(e))
    return 0


# функция для распознавания речи из файла
def recognize_from_file(audio_file):
    audio_file = ogg_to_wav(audio_file)  # преобразование файла в формат WAV
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, show_all=True)
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition не может понять аудио")
    except sr.RequestError as e:
        print("Не удается запросить результаты из службы Google Speech Recognition; {0}".format(e))
    return False
