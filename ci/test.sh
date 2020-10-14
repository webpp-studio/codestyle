#!/bin/bash

echo "Запуск тестирования приложения..."
docker run --rm codestyle-test

echo "Проверка качества кода приложения..."
docker run --rm --volume `pwd`:/code:ro --workdir /code codestyle ./codestyle ./tests ./setup.py --exclude ./codestyle/tool_settings
