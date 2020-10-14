"""Проверки модуля с настройками."""
from unittest import TestCase

from codestyle.settings import get_logging_config


class Test(TestCase):
    """Проверки функций модуля."""

    def test_get_logging_config(self):
        """Проверка get_logging_config."""
        mock_line_separator = '\n'
        mock_logging_level = 'INFO'
        result_config = get_logging_config(
            mock_line_separator, mock_logging_level
        )
        expected_config = {
            'version': 1,
            'formatters': {
                'standard': {
                    'format': '\033[1m{message}\033[0m\n',
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
                'codestyle': {
                    'handlers': ['standard_handler'],
                    'propagate': False,
                    'level': 'INFO',
                },
            },
            'disable_existing_loggers': True,
        }
        self.assertDictEqual(expected_config, result_config)
