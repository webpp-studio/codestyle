"""Модуль с приложением."""
from collections import defaultdict
from functools import lru_cache
from logging import ERROR, INFO, Logger, getLogger
from pathlib import Path
from typing import Callable, Dict, List, Type

from codestyle.code_path import ExpandedPathTree
from codestyle.parameters_parse import ParametersStorage
from codestyle.system_wrappers import ExitCodes, interrupt_program_flow
from codestyle.tool_wrappers import (Autoflake, Autopep8, ConsoleTool, ESLint,
                                     Flake8, HTMLCS, PHPCBF, PHPCS, Result,
                                     TOOL_SETTINGS_PATH, Stylelint,
                                     MyPy, Black, ShellCheck)

FIX_SUCCESS = 'Твой код просто огонь!💥 Мне не пришлось ничего исправлять.'
FIX_UNSUCCESSFUL = ('Проверено файлов - {total_count}, из них было '
                    'исправлено - {total_failed}.')
CHECK_SUCCESS = ('Я проверил твои файлы ({total_count} шт.), можешь не '
                 'беспокоиться об их качестве. ✨ 💥')
CHECK_UNSUCCESSFUL = ('💔 Так-так-таак... Коллегам не стыдно в глаза '
                      'смотреть? Необходимо поправить файлов: '
                      '{total_failed}.')
MESSAGES = {'fix': {ExitCodes.SUCCESS: FIX_SUCCESS,
                    ExitCodes.UNSUCCESSFUL: FIX_UNSUCCESSFUL},
            'check': {ExitCodes.SUCCESS: CHECK_SUCCESS,
                      ExitCodes.UNSUCCESSFUL: CHECK_UNSUCCESSFUL}}
ENABLED_TOOLS = (Flake8, Autopep8, Autoflake, ESLint, PHPCS, PHPCBF, HTMLCS,
                 Stylelint, MyPy, Black, ShellCheck)


# TODO еще надо глянуть почему долго запускается, найти проблемные места
class ConsoleApplication:
    """Консольное приложение."""

    logger: Logger = getLogger(__name__)

    def __init__(self, parameters_storage: ParametersStorage):
        """
        Подготовка приложения к выполнению.

        :param parameters_storage: Хранилище параметров, извлечённых из
            командной строки и/или файла конфигурации.
        """
        self.__parameters_storage = parameters_storage
        method = 'fix' if self.__parameters_storage.fix else 'check'
        self.__process_method = method
        self.__file_suffix_tools = self.get_file_suffix_tools()

        self.logger.debug('Разворачивание дерева файлов и директорий...')
        path_tree = ExpandedPathTree(
            *self.__parameters_storage.target,
            excludes=self.__parameters_storage.exclude)
        self.__path_gen = path_tree.path_gen()

        self.logger.debug('Определение метода обработки файлов...')
        self.__status_messages = MESSAGES[self.__process_method]

    @lru_cache(maxsize=None)
    def get_tool(self, cls: Type[ConsoleTool]) -> ConsoleTool:
        """
        Получить инстанс инструмента.

        :param cls: класс инструмента
        :return:
        """
        return cls(**self.__get_tool_kwargs(cls))

    def process_files(self):
        """Обработка файлов."""
        self.logger.info('Запуск обработки файлов...')

        total_success = total_failed = 0
        status, log_level = ExitCodes.SUCCESS, INFO

        for path in self.__path_gen:
            for tool_cls in self.__file_suffix_tools.get(path.suffix, []):
                tool = self.get_tool(tool_cls)
                process_method = getattr(tool, self.__process_method)
                result = self.__process_file(path, process_method)
                if result.is_success:
                    total_success += 1
                else:
                    total_failed += 1
        if total_failed > 0:
            status, log_level = ExitCodes.UNSUCCESSFUL, ERROR

        message = self.__status_messages[status].format(
            total_count=(total_failed + total_success),
            total_failed=total_failed)
        interrupt_program_flow(status=status, log_message=message,
                               log_level=log_level)

    def __tool_can_process(self, tool: ConsoleTool) -> bool:
        """Проверка возможностей указанного инструмента."""
        can_process = getattr(tool, f'for_{self.__process_method}', False)
        if getattr(self.__parameters_storage, tool.optional_flag, False):
            return can_process

        return can_process and not tool.optional

    def __process_file(self, file_path: Path,
                       process_method: Callable) -> Result:
        """
        Обработка указанного файла с переданным методом.

        :param file_path: Путь обрабатываемого файла.
        :param process_method: Метод обработки (fix() / check()).
        :return: Результат обработки файла.
        """
        self.logger.info(f'Обработка {file_path}..')
        result = process_method(str(file_path))

        if result.whole_output:
            level = INFO if result.is_success else ERROR
            self.logger.log(level, result.whole_output)
        return result

    def get_file_suffix_tools(self) -> Dict[str, List[ConsoleTool]]:
        """
        Создание словаря с расширениями файлов.

        :param tools: набор утилит
        :return: словарь с расширениями, каждому из которых
            соответствует свой набор поддерживаемых утилит
        """
        file_suffix_tools = defaultdict(list)
        tools = filter(self.__tool_can_process, ENABLED_TOOLS)
        for tool in tools:
            for suffix in tool.supported_file_suffixes:
                file_suffix_tools[suffix].append(tool)

        return file_suffix_tools

    def __get_tool_kwargs(self, tool_wrapper) -> dict:
        """
        Определение kwarg'ов для инициализации инструмента.

        :param tool_wrapper: Инструмент.
        :return: Словарь с kwarg'ами.
        """
        tool_kwargs = {'configuration_path': None}

        if self.__parameters_storage.settings != TOOL_SETTINGS_PATH:
            configuration_path = self.__get_config_path(
                tool_wrapper, self.__parameters_storage.settings)
            tool_kwargs.update({'configuration_path': str(configuration_path)})

        if tool_wrapper.cli_tool_name in ('phpcs', 'phpcbf'):
            tool_kwargs.update(
                {'encoding': self.__parameters_storage.phpcs_encoding})

        return tool_kwargs

    def __get_config_path(self, tool_wrapper, settings_path: Path) -> Path:
        """
        Определение пути к конфигурации для указанного инструмента.

        :param tool_wrapper: Инструмент.
        :param settings_path: Путь до установленных стандартов.
        :return: Путь к конфигурации.
        """
        storage_configuration = getattr(
            self.__parameters_storage,
            tool_wrapper.get_name() + '_configuration')
        return settings_path / storage_configuration
