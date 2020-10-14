#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Сборка codestyle образа..."
docker build --tag codestyle "$DIR/.."

echo "Сборка образа для тестирования..."
docker build --file tests/Dockerfile --tag codestyle-test "$DIR/.."
