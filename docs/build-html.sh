#!/usr/bin/env bash

# Сборка документации в виде HTML файлов в _build директорию
pyenv exec sphinx-build -a -W . _build
