"""Модуль командной строки."""
from logging import WARNING
from logging.config import dictConfig

from codestyle.application import ConsoleApplication
from codestyle.parameters_parse import ArgumentationTool, ParametersStorage
from codestyle.settings import get_logging_config
from codestyle.system_wrappers import ExitCodes, interrupt_program_flow


def run_process():
    """Запуск процесса обработки файлов."""
    arg_tool = ArgumentationTool()
    parameters_storage: ParametersStorage = arg_tool.parameters_storage
    dictConfig(get_logging_config(parameters_storage.line_separator,
                                  parameters_storage.logging_level))

    try:
        ConsoleApplication(parameters_storage).process_files()
    except KeyboardInterrupt:
        interrupt_program_flow(status=ExitCodes.UNSUCCESSFUL,
                               log_message='Проверка прервана.',
                               log_level=WARNING)
