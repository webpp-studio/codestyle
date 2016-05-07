FROM ubuntu:14.04

RUN apt-get update -qq && apt-get install -yq \
    python-pip nodejs npm php-pear
RUN npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion
RUN pear install PHP_CodeSniffer
RUN ln -s /usr/bin/nodejs /usr/bin/node
COPY . /tmp/codestyle
RUN cd /tmp/codestyle && python setup.py install
RUN rm -rf /tmp/codestyle

ENTRYPOINT ["codestyle"]
