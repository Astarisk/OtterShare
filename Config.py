import configparser
from pathlib import Path

config = configparser.ConfigParser()
config_file = Path('config.ini')

save_hotkey = 'p'
save_location = 'C:\\Users\\Keith\\Desktop\\testsaves\\'
save_as_png = 'True'
if not config_file.is_file():
    config['DEFAULT'] = {'save_image_hotkey': 'p', 'save_location': 'C:\\Users\\Keith\\Desktop\\testsaves\\',
                         'save_as_png': 'True'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_file)
    save_hotkey = config['DEFAULT']['save_image_hotkey']
    save_location = config['DEFAULT']['save_location']
    save_as_png = config['DEFAULT']['save_as_png']
