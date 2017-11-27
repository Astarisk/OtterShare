import configparser
from pathlib import Path
import os

config = configparser.ConfigParser()
config_file = Path('config.ini')

# In order to upload the file to imgur, you will need to register the program through them to get a clientid
client_id = ''
save_hotkey = 'ctrl+shift+e'
# Going to save the files to the CWD for now
save_location = os.getcwd() + '\\testsaves\\'

save_as_png = 'True'  # TODO: I think I'll just force a png save, change this later if I make up my mind.
save_img = 'True'
upload_img = 'True'

if not config_file.is_file():
    config['DEFAULT'] = {'client_id': '', 'save_image_hotkey': save_hotkey,
                         'save_location': save_location,
                         'save_as_png': 'True',
                         'save_img': 'True',
                         'upload_img': 'True'}
    save_hotkey = set(save_hotkey.split('+'))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_file)
    client_id = config['DEFAULT']['client_id']

    save_hotkey = config['DEFAULT']['save_image_hotkey']
    save_hotkey = set(save_hotkey.split('+'))

    save_location = config['DEFAULT']['save_location']

    save_as_png = config['DEFAULT']['save_as_png']
    save_img = config['DEFAULT']['save_img']
    upload_img = config['DEFAULT']['upload_img']


def save_path_location():
    os.makedirs(save_location, exist_ok=True)
    return save_location
