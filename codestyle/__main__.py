"""
Главный модуль проекта, альтернатива выражению if __name__ == '__main__'.

Его наличие даёт возможность запускать приложение из командной строки
средствами Python с флагом -m.
Подробнее: https://docs.python.org/3.8/library/__main__.html
"""
from codestyle.command_line import run_process

run_process()
