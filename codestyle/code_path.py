"""Модуль с генератором путей к файлам."""
from logging import CRITICAL, getLogger
from pathlib import Path
from typing import Generator, Iterable

from codestyle.system_wrappers import ExitCodes, interrupt_program_flow


class ExpandedPathTree:
    """Развёрнутое дерево путей к файлам."""

    def __init__(self, *targets, excludes: Iterable[str] = ()):
        """
        Создание объекта.

        :param targets: пути в файловой системе
        :param excludes: исключаемые из генератора пути
        """
        self.check_path_availability(targets)
        self.targets = set(targets)
        self.excludes = set(excludes)

    @property
    def path_generator(self) -> Generator[Path, None, None]:
        """Генератор развёрнутых путей."""
        for path in self.targets:
            yield from self.__generate_paths(path)

    @staticmethod
    def check_path_availability(paths: Iterable[Path]):
        """
        Проверка доступности указанных путей.

        Если путь недоступен - работа приложения завершается со статусом
            ExitCodes.UNSUCCESSFUL
        """
        getLogger(__name__).info('Проверяю какие тут пути ты мне указал...')
        missing_paths = filter(lambda path: not path.exists(), paths)
        for path in missing_paths:
            interrupt_program_flow(status=ExitCodes.UNSUCCESSFUL,
                                   log_message=f'Путь {path} недоступен.',
                                   log_level=CRITICAL)

    def __is_excluded(self, path: Path) -> bool:
        """Проверка исключён путь или нет."""
        for exclude in self.excludes:
            if path.match(exclude):
                return True
        return False

    def __generate_paths(self, path: Path) -> Generator[Path, None, None]:
        """
        Генерация путей с проверкой доступности в файловой системе.

        :param path: путь до файла или директории
        :return: генератор путей до файлов
        """
        if self.__is_excluded(path):
            return
        if path.is_file():
            yield path
        else:
            for directory_child in path.iterdir():
                yield from self.__generate_paths(directory_child)
