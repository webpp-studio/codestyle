FROM python:3.6-slim-buster

COPY . /usr/src/app

RUN cd /usr/src/app && \
    apt-get -q update && \
    apt-get -qy install --no-install-recommends curl && \
    pip3 install tox && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get -qy install --no-install-recommends python3.7 python3-distutils \
        nodejs php-pear && \
    npm -g install stylelint htmlcs walk brace-expansion eslint && \
    npm install eslint eslint-plugin-vue && \
    pear channel-update pear.php.net && \
    pear install PHP_CodeSniffer && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

CMD ["tox"]