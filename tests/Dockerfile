FROM python:3.6-slim-buster

RUN apt-get -q update && \
    apt-get -qy install --no-install-recommends curl && \
    pip3 install tox && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get -qy install --no-install-recommends python3.7 python3-distutils \
        nodejs php-pear && \
    pear channel-update pear.php.net && \
    pear install PHP_CodeSniffer && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app

RUN cd /usr/src/app \
    && mkdir -p /npm/node_modules \
    && cat npm-deps.txt | xargs npm -g install \
    && cd / && rm -rf /tmp/*


WORKDIR /usr/src/app
CMD ["tox"]