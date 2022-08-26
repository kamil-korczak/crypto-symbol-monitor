import configparser

CONFIG_SRC = 'src/config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_SRC)

SYMBOLS_SRC = config['SYMBOLS']['SRC']
