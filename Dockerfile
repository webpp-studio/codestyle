FROM alpine:3.10
COPY . /tmp/codestyle
RUN \
    set -ex && \
    cd /tmp/codestyle && \
    apk add --quiet --progress --no-cache \
            python3=~3.7 npm php7-pear php7-openssl php7-tokenizer \
            php7-xmlwriter php7-simplexml && \
    python3 setup.py --quiet install && \
    npm install --production --global --no-optional \
                jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion && \
    npm cache --force clean && \
    pear channel-update pear.php.net && \
    pear install --soft --onlyreqdeps PHP_CodeSniffer && \
    cd / && rm -rf /tmp/*
ENTRYPOINT ["codestyle"]