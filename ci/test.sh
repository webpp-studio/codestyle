#!/bin/bash

# Run tests
docker run --rm --volume=`pwd`:/code --workdir=/code \
    --entrypoint=/usr/bin/python codestyle runtests.py

# Self-checking (codestyle)
docker run --rm --volume=`pwd`:/code --workdir=/code codestyle . \
    --exclude=./tests/data

# Check codestyle of the single script without extension
docker run --rm --volume=`pwd`:/code --workdir=/code codestyle \
    --language=py ./scripts/codestyle
