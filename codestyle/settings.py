"""Настройки приложения."""
import codestyle


def get_logging_config(line_separator: str, logging_level: str) -> dict:
    """Получение конфигурации логирования с учётом передаваемых параметров."""
    bold_sequence = '\033[1m'  # добавляет тексту жирное начертание
    reset_style_sequence = '\033[0m'  # сбрасывает стили выше
    logging_format = (
        bold_sequence + '{message}' + reset_style_sequence + line_separator)
    return {
        'version': 1,
        'formatters': {
            'standard': {
                'format': logging_format,
                'style': '{',
            }
        },
        'handlers': {
            'standard_handler': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            codestyle.__name__: {
                'handlers': ['standard_handler'],
                'propagate': False,
                'level': logging_level,
            },
        },
        'disable_existing_loggers': True,
    }
