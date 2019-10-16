FROM python:3.7
COPY . /tmp/codestyle
RUN \
    cd /tmp/codestyle && \
    python3 setup.py install && \
    apt-get -q update && \
    apt-get -qy install --no-install-recommends nodejs npm php-pear && \
    npm install -g jshint jscs jscs-fixer csscomb htmlcs walk brace-expansion && \
    pear channel-update pear.php.net && \
    pear install PHP_CodeSniffer && \
    rm -rf /var/lib/apt/lists/* /tmp/codestyle
ENTRYPOINT ["codestyle"]