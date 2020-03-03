FROM php:7.3-cli-alpine3.10

RUN apk add --quiet --progress --no-cache python3=~3.7 npm && \
    pear install --soft --onlyreqdeps PHP_CodeSniffer

COPY . /tmp/codestyle

RUN cd /tmp/codestyle \
    && python3 setup.py --quiet install

RUN cd /tmp/codestyle \
    && mkdir -p /npm/node_modules \
    && cat npm-deps.txt | xargs npm -g install \
    && cd / && rm -rf /tmp/*
ENTRYPOINT ["codestyle"]