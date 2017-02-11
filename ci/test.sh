#!/bin/bash

echo "Running tests..."
# Run tests
docker run --rm --volume=`pwd`:/code --workdir=/code \
    --entrypoint=/usr/bin/python codestyle setup.py test || exit $?
echo

echo "Checking a self codestyle..."
# Self-checking (codestyle)
docker run --rm --volume=`pwd`:/code:ro --workdir=/code codestyle \
    ./codestyle ./tests ./runtests.py \
    --exclude ./tests/data || exit $?
echo

echo "Checking a self codestyle for scripts..."
# Check codestyle of the single script without extension
docker run --rm --volume=`pwd`:/code:ro --workdir=/code codestyle \
    --language=py ./scripts/codestyle || exit $?