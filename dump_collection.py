from pickle import dump, load
from constants import collections_path


def add_collection(name, wordlist):
    with open(wordlist) as file:
        collection = file.readlines()
    collection = [word.replace('\n', '') for word in collection]
    path = f'collection_{name}.pkl'
    print(collection[:5])
    with open(f'{collections_path}{path}.pkl', 'wb') as file:
        dump(collection, file)
    print(f'Dumped in {collections_path}{path} successful')


add_collection('main', 'words.txt')