"""Парсинг параметров из командной строки и конфигурационного файла."""
from os import linesep
from pathlib import Path
from typing import Tuple

from configargparse import ArgumentParser, Namespace, DefaultConfigFileParser

from codestyle import (__name__ as application_name,
                       __description__ as application_description)
from codestyle.parameters import PARAMETERS


class ParametersStorage(Namespace):
    """
    Хранилище параметров.

    Заполняется из конфигурационного файла и командной строки.
    """

    @property
    def line_separator(self) -> str:
        """Разделитель строк с учётом compact параметра."""
        return '' if getattr(self, 'compact', False) else linesep

    @property
    def logging_level(self) -> str:
        """
        Уровень логирования с учётом debug и quiet параметров.

        Для включенного режима отладки уровень логирования всегда DEBUG;
        в ином случае - WARNING если включен тихий режим (quiet),
        по-умолчанию в следующем приоритете - INFO.
        """
        if getattr(self, 'debug', False):
            return 'DEBUG'
        if getattr(self, 'quiet', False):
            return 'WARNING'
        return 'INFO'


class ArgumentationTool:
    """
    Инструмент для добавления аргументов.

    Набор аргументов описан в модуле parameters_parse.
    """

    PARAMETERS_FILE_NAME = f'.{__package__}.cfg'
    USER_PARAMETERS_PATH = Path(PARAMETERS_FILE_NAME).expanduser().absolute()
    IN_CWD_PARAMETERS_PATH = Path.cwd().absolute() / PARAMETERS_FILE_NAME
    DEFAULT_CONFIG_FILES: Tuple[str, ...] = (str(USER_PARAMETERS_PATH),
                                             str(IN_CWD_PARAMETERS_PATH))

    def __init__(self):
        """Подготовка инструмента для работы с параметрами."""
        self.__argument_parser = ArgumentParser(
            add_env_var_help=False,
            config_file_parser_class=DefaultConfigFileParser,
            default_config_files=self.DEFAULT_CONFIG_FILES,
            prog=application_name,
            description=application_description)

        self.__define_parameters()
        self.parameters_storage, _ = self.__argument_parser.parse_known_args(
            namespace=ParametersStorage())

    def __define_parameters(self):
        """Добавление параметров."""
        for arguments, options in PARAMETERS:
            self.__argument_parser.add_argument(*arguments, **options)
