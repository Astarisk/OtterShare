import configparser
from pathlib import Path
import os

config = configparser.ConfigParser()
config_file = Path(os.getcwd() + '\\config.ini')


keys = {
    'client_id': '',
    'save_hotkey': 'ctrl+shift+e',
    'save_location':  os.getcwd() + '\\testsaves\\',
    'save_img': 'True',
    'upload_img': 'True',
    'area_select_picture': 'ctrl+shift+t'
}


def load_config():
    config.read(config_file)
    for key in keys:
        keys[key] = config['DEFAULT'][key]


if not config_file.is_file():
    config['DEFAULT'] = keys
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    load_config()


def grab_value(key):
    return config['DEFAULT'][key]


def get_client_id():
    return keys['client_id']


def get_save_hotkey():
    combo = set(keys['save_hotkey'].split('+'))
    return combo


def get_save_location():
    return keys['save_location']


def get_save_img():
    return keys['save_img']


def get_upload_img():
    return keys['upload_img']
