from pickle import dump, load
from constants import collections_path
import os

# Словарь для хранения путей к коллекциям
collections = {'главная': f'collection_main.pkl'}


# Функция для записи словаря collections в файл
def dump_collections():
    global collections
    with open(f'{collections_path}collections.pkl', 'wb') as file:
        dump(collections, file)


# Функция для чтения словаря collections из файла
def load_collections():
    global collections
    with open(f'{collections_path}collections.pkl', 'rb') as file:
        collections = load(file)


# Функция для добавления коллекции в словарь collections
def add_collection(name, collection):
    global collections
    name = name.lower()
    path = f'collection_{len(collections)}.pkl'
    collections[name] = path
    dump_collections()
    with open(f'{collections_path}{path}', 'wb') as file:
        dump(collection, file)


# Функция для получения коллекции по ее имени
def get_collection(name):
    global collections
    name = name.lower()
    if name not in collections:  # Если коллекция не найдена, возвращается основная коллекция
        return get_collection('главная')
    path = collections_path + collections[name]
    with open(path, 'rb') as file:
        collection = load(file)
    return collection


# Функция для получения списка пользовательских коллекций по id пользователя
def get_user_collections(user_id):
    path = f'{collections_path}u{user_id}_coll.pkl'
    if not os.path.isfile(path):
        return {}
    with open(path, 'rb') as file:
        user_collections = load(file)
    return user_collections


def get_formatted_collections(user_id):
    user_collections = get_user_collections(user_id)
    if len(user_collections) == 0:
        return ''
    formatted_collections = '\n'.join([f'{i+1}. ' +
                                       (word[0].upper() + word[1:]) for i, word in enumerate(user_collections)])
    formatted_collections = f'\nСписок созданных вами подборок:\n{formatted_collections}\n' + \
                            '\nЧтобы выбрать подборку, напишите её название'
    return formatted_collections


# Функция для сохранения пользовательской коллекции
def save_user_collection(user_id, collection, name):
    user_collections = get_user_collections(user_id)
    name = name.lower()
    if name not in user_collections:
        user_collections[name] = collection
    with open(f'{collections_path}u{user_id}_coll.pkl', 'wb') as file:
        dump(user_collections, file)
    collection_path = list(user_collections.keys()).index(name)
    with open(f'{collections_path}u{user_id}_c{collection_path}.pkl', 'wb') as file:
        dump(collection, file)


# Функция для загрузки пользовательской коллекции
def load_user_collection(user_id, name):
    user_collections = get_user_collections(user_id)
    if name.isnumeric():
        path = f'{collections_path}u{user_id}_c{user_collections[list(user_collections.keys())[int(name)]]}.pkl'
        with open(path, 'rb') as file:
            collection = load(file)
        return collection
    name = name.lower()
    if name not in user_collections: # Если не найдена, возвращается основная коллекция
        return get_collection('главная')
    collection_path = list(user_collections.keys()).index(name)
    with open(f'{collections_path}u{user_id}_c{collection_path}.pkl', 'rb') as file:
        collection = load(file)
    return collection
