import logging

GENERAL_TEXT = 'general'
DEBUG_TEXT = 'debug'

DEBUG_INT_TRUE = 1
DEBUG_INT_FALSE = 0

LOGGER = {
    'format_type': {
        DEBUG_INT_TRUE: DEBUG_TEXT,
        DEBUG_INT_FALSE: GENERAL_TEXT,
    },
    'level': {
        DEBUG_INT_TRUE: logging.DEBUG,
        DEBUG_INT_FALSE: logging.INFO,
    }
}


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

FORMATTER = {
    logging.INFO: {
        GENERAL_TEXT: '%(asctime)s |%(color_on)s %(message)s %(color_off)s',
        DEBUG_TEXT: '%(asctime)s |%(color_level)s %(levelname)s %(color_off)s| %(module)s |%(color_on)s %(message)s %(color_off)s',
    },
    GENERAL_TEXT: {
        GENERAL_TEXT: '%(asctime)s |%(color_level)s %(levelname)s %(color_off)s|%(color_on)s %(message)s %(color_off)s',
        DEBUG_TEXT: '%(asctime)s |%(color_level)s %(levelname)s %(color_off)s| %(module)s |%(color_on)s %(message)s %(color_off)s',
    }
}


class LoggingFormatter(logging.Formatter):

    # COLOR_CODES = { logging.levelno: [ color_on, color_log_level ]}
    COLOR_CODES = {
        # [red/bold, red_bg:black/bold]
        logging.CRITICAL: ["\033[31;1m", '\033[1;30;41m'],
        # [red, red_bg:grey/light]
        logging.ERROR:    ["\033[31;20m", '\033[1;41m'],
        # [grey_bg:black, grey_bg:black/light]
        logging.WARNING:  ["\033[1;33m", "\033[30;43m"],
        # [grey/light, green_bg:grey/light]
        logging.INFO:     ["\033[38;20m", '\033[42m'],
        # [red/bold, red_bg:black/bold]
        logging.DEBUG:    ["\033[38;20m", '\033[30;47m']
    }

    RESET_CODE = "\033[0m"

    def __init__(self, formatter_type, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter_type = formatter_type
        self.color = color

    def format(self, record, *args, **kwargs):

        if self.color is True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno][0]
            record.color_level = self.COLOR_CODES[record.levelno][1]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_level = ""
            record.color_off = ""

        if record.levelno in FORMATTER:
            formatter_dict_key = record.levelno
        else:
            formatter_dict_key = GENERAL_TEXT

        self._style._fmt = FORMATTER[formatter_dict_key][self.formatter_type]

        formatter_ = super().format(record, *args, **kwargs)

        return formatter_


def create_logger(app):

    # Create log formatter
    formatter = LoggingFormatter(formatter_type=LOGGER['format_type'][app.debug],
                                 color=True,
                                 datefmt=DATE_FORMAT)

    # Create logger with name
    logger = logging.getLogger(app.name)

    # Set logger level
    logger.setLevel(LOGGER['level'][app.debug])

    # Initiate console handler
    console_handler = logging.StreamHandler()

    # Set formatter for console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger
