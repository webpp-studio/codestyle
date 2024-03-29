![image](https://git.webpp.ru/tools/codestyle/badges/master/coverage.svg)

Инструмент проверки кода
========================

Поддерживает несколько языков (проверяет или исправляет):

-   PHP (phpcs, phpcbf)
-   Python (flake8, autopep8, autoflake)
-   Javascript (eslint)
-   CSS (stylelint)
-   HTML (htmlcs)

Консольные аргументы приложения
-------------------------------

 Аргумент | Описание
--- | ---
`-h, --help` | Отобразить вспомогательное сообщение и завершить работу программы
`-f, --fix` | Исправить ошибки по возможности
`-c, --compact` | Включить компактный вывод процесса работы приложения
`-q, --quiet` | Включить тихий режим работы приложения (показывать только ошибки)
`-d, --debug` | Включить режим отладки
`-s SETTINGS, --settings SETTINGS` | Путь до директории с настройками инструментов (по умолчанию: ./tool_settings)
`--file_suffix <file_suffix>` | Проверяемое расширение файлов (.py, .js и так далее; по-умолчанию: все расширения)
`-m, --mypy` |  Опциональная проверка типизации при помощи mypy
`-b, --black` | Опциоанльное форматирование при помощи black, только после флага -f
`-hl, --hadolint` |  Опциональная проверка Dockerfile`ов, в файле .hadolint.yaml указать: ignored: - <номер ошибки>
`-x <globbing шаблон>, --exclude <globbing шаблон>` | Исключить по указанному globbing шаблону, для файла необходимо указывать список exclude = [file1, file2, ...]
`--phpcs-encoding PHPCS_ENCODING` | Кодировка для PHP_CodeSniffer (по-умолчанию: utf-8)
`--stylelint-configuration_name STYLELINT_CONFIGURATION` | Имя файла конфигурации для stylelint утилиты (по-умолчанию: .stylelintsrc.json)
`--phpcbf-configuration_name PHPCBF_CONFIGURATION` | Имя файла конфигурации для phpcbf утилиты (по-умолчанию: phpcs.xml)
`--phpcs-configuration_name PHPCS_CONFIGURATION` | Имя файла конфигурации для phpcs утилиты (по-умолчанию: phpcs.xml
`--flake8-configuration_name FLAKE8_CONFIGURATION` | Имя файла конфигурации для flake8 утилиты (по-умолчанию: flake8.conf
`--htmlcs-configuration_name HTMLCS_CONFIGURATION` | Имя файла конфигурации для htmlcs утилиты (по-умолчанию: htmlcs.json
`--eslint-configuration_name ESLINT_CONFIGURATION` | Имя файла конфигурации для cssbomb утилиты (по-умолчанию: eslint.json)
`-v, --version` | Отобразить версию приложения и завершить работу программы

Порядок использования консольных аргументов приложения
------------------------------------------------------

``` {.sourceCode .console}
codestyle [-h] [-f] [-c] [-q] [-d] [-s SETTINGS] [--file_suffix <file suffix>]
          [-x <globbing шаблон> [<globbing шаблон> ...]] [--phpcs-encoding PHPCS_ENCODING]
          [--stylelint-configuration_name STYLELINT_CONFIGURATION]
          [--phpcbf-configuration_name PHPCBF_CONFIGURATION] [--phpcs-configuration_name PHPCS_CONFIGURATION]
          [--flake8-configuration_name FLAKE8_CONFIGURATION] [--htmlcs-configuration_name HTMLCS_CONFIGURATION]
          [--eslint-configuration_name ESLINT_CONFIGURATION] [-v] target [target ...]
```

### Использование в качестве устанавливаемого приложения

#### Требования

-   NPM
    :   -   [eslint](https://github.com/eslint/eslint)
        -   [eslintppluginvvue](https://github.com/vuejs/eslint-plugin-vue)
        -   [stylelint](https://github.com/stylelint/stylelint)
        -   [htmlcs](https://www.npmjs.com/package/htmlcs)

-   [PHPCCodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer)
-   Python (3.6 / 3.7 / 3.8 / 3.9) и pip

#### Установка

``` {.sourceCode .console}
./setup.py install
```

#### Пример использования

``` {.sourceCode .console}
python -m codestyle /checking_directory --compact --quiet --exclude /checking_directory/dirty.py
```

### Использование в Docker контейнере

#### Сборка образа

``` {.sourceCode .console}
docker build --tag codestyle:latest .
```

#### Пример использования

``` {.sourceCode .console}
docker run --volume <checking_directory>:/code --workdir /code --tty codestyle:latest /code --exclude /code/dirty.py
```

### Процесс разработки с docker-compose

#### Сборка образа

``` {.sourceCode .console}
docker-compose build
```

#### Запуск

``` {.sourceCode .console}
docker-compose run cli-tool <консольные аргументы приложения, перечисленные выше>
```

#### Обновление документации для Sphinx (вне контейнера)

``` {.sourceCode .console}
python -m install sphinx
sphinx-apidoc --force --separate --no-toc --module-first --output-dir docs/pages codestyle codestyle/tool_settings
```
