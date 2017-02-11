FROM ubuntu:14.04

RUN apt-get update -qq && apt-get install -yq \
    python3 python3-pip nodejs npm php-pear python-setuptools python3-setuptools
RUN npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion
RUN pear install PHP_CodeSniffer
RUN ln -s /usr/bin/nodejs /usr/bin/node
COPY . /tmp/codestyle

RUN pip3 install --upgrade pip setuptools

RUN cd /tmp/codestyle && python3 setup.py install
RUN rm -rf /tmp/codestyle

ENTRYPOINT ["codestyle"]
