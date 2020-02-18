FROM php:7.3-cli-alpine3.10
COPY . /tmp/codestyle
RUN \
    set -eux && \
    cd /tmp/codestyle && \
    apk add --quiet --progress --no-cache \
            python3=~3.7 npm && \
    python3 setup.py --quiet install && \
    npm install --production --global --no-optional stylelint htmlcs walk \
            brace-expansion eslint && \
    npm cache --force clean && \
    pear install --soft --onlyreqdeps PHP_CodeSniffer && \
    cd / && rm -rf /tmp/*
ENTRYPOINT ["codestyle"]