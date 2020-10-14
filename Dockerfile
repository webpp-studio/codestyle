FROM php:7.4.10-cli-alpine3.12
RUN apk add --purge --no-cache python3=3.8.5-r0 py3-pip=20.1.1-r0 npm=12.18.4-r0 \
    && pear channel-update pear.php.net \
    && pear install PHP_CodeSniffer-3.5.6 \
    && python3 -m pip --no-cache-dir install wheel==0.35.1
WORKDIR /app
COPY . /tmp/app
RUN mv /tmp/app/package*.json . \
    && npm install \
    && cd /tmp/app \
    && ./setup.py install \
    && rm -r /tmp/*
ENV PATH /app/node_modules/.bin/:$PATH
ENTRYPOINT ["python3", "-m", "codestyle"]
