"""Набор вспомогательных инструментов для взаимодействия с ОС."""
import sys
from enum import IntEnum
from logging import INFO, getLogger
from subprocess import (CalledProcessError, TimeoutExpired,  # noqa: S404
                        check_output as check_process_output)
from typing import Optional

from codestyle import FIRST_ELEMENT_INDEX


_logger = getLogger(__name__)


class ExitCodes(IntEnum):
    """Коды завершения работы программы."""

    SUCCESS: int = 0
    UNSUCCESSFUL: int = 1


def interrupt_program_flow(status: int = ExitCodes.SUCCESS,
                           log_message: str = None, log_level: int = INFO):
    """Завершение работы программы с возможностью вывода сообщения."""
    if log_message:
        _logger.log(log_level, log_message)

    sys.exit(status)


def check_output(run_arguments: tuple) -> Optional[str]:
    """Получение результата работы программы с запускаемыми аргументами."""
    tool_name = run_arguments[FIRST_ELEMENT_INDEX]
    try:
        _logger.debug(f'Проверка наличия {tool_name} в системе...')
        return check_process_output(run_arguments,  # noqa: S603
                                    timeout=10).decode().rstrip()
    except (CalledProcessError, FileNotFoundError, TimeoutExpired) as error:
        _logger.warning(f'Инструмент {tool_name} не найден.')
        _logger.debug(str(error))

        interrupt_program_flow(ExitCodes.UNSUCCESSFUL)
