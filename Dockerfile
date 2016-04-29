FROM ubuntu:14.04

RUN apt-get update -qq && apt-get install -yq \
    python-pip npm php-pear
RUN pip install codestyle
RUN npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion
RUN pear install PHP_CodeSniffer

ENTRYPOINT ["codestyle"]
