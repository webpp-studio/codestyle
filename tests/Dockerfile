FROM ubuntu:18.04

RUN apt update -qq && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt install -y -qq python3 python3.5 python3.6 python3-pip php-pear python-setuptools python3-setuptools nodejs npm && \
    pip3 install tox && \
    npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion && \
    pear install PHP_CodeSniffer

COPY . /app
WORKDIR /app

CMD tox