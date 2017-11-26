import configparser
from pathlib import Path

config = configparser.ConfigParser()
config_file = Path('config.ini')

client_id = ''
save_hotkey = 'p'
save_location = 'C:\\Users\\Keith\\Desktop\\testsaves\\'
save_as_png = 'True'  # TODO: I think I'll just force a png save, change this later if I make up my mind.
save_img = 'True'
upload_img = 'True'

if not config_file.is_file():
    config['DEFAULT'] = {'client_id': '', 'save_image_hotkey': 'p',
                         'save_location': 'C:\\Users\\Keith\\Desktop\\testsaves\\',
                         'save_as_png': 'True',
                         'save_img': 'True',
                         'upload_img': 'True'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_file)
    client_id = config['DEFAULT']['client_id']
    save_hotkey = config['DEFAULT']['save_image_hotkey']
    save_location = config['DEFAULT']['save_location']
    save_as_png = config['DEFAULT']['save_as_png']
    save_img = config['DEFAULT']['save_img']
    upload_img = config['DEFAULT']['upload_img']
