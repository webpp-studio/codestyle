"""Модуль с генератором путей к файлам."""
from logging import CRITICAL, getLogger
from pathlib import Path
from typing import Generator, Iterable


_logger = getLogger(__name__)


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

    def path_gen(self, targets=None) -> Generator[Path, None, None]:
        """Генератор развёрнутых путей."""
        targets = targets if targets else self.targets
        for path in targets:
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
            _logger.log(CRITICAL, f'Путь {path} недоступен.')

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
        elif path.is_dir():
            yield from self.path_gen(path.iterdir())
