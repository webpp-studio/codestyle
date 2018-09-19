FROM ubuntu:16.04

RUN apt-get update -qq && \
    apt-get install -y software-properties-common -qq && \
    add-apt-repository ppa:fkrull/deadsnakes -y && \
    apt-get update -qq && \
    apt-get install -qq python3 python3.5 python3.6 python3-pip nodejs php-pear python-setuptools python3-setuptools nodejs npm && \
    pip3 install tox && \
    npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion && \
    pear install PHP_CodeSniffer

COPY . /app
WORKDIR /app

CMD tox