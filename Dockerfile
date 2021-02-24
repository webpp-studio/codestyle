FROM php:7.4.10-cli-alpine3.12
RUN apk add --purge --no-cache python3=3.8.5-r1 py3-pip=20.1.1-r0 npm=12.21.0-r0 musl-dev python3-dev gcc \
    && pear channel-update pear.php.net \
    && pear install PHP_CodeSniffer-3.5.6 \
    && python3 -m pip --no-cache-dir install wheel==0.35.1 \
    && apk add shellcheck \
    && wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.22.1/hadolint-Linux-x86_64
WORKDIR /app
COPY . /tmp/app
RUN cd /tmp/app \
    && cat npm-deps.txt | xargs npm -g install \
    && ./setup.py install \
    && cp /tmp/app/codestyle/tool_settings/.shellcheckrc /root \
    && cp /tmp/app/codestyle/tool_settings/.hadolint.yaml /app \
    && rm -r /tmp/* \
    && chmod +x /bin/hadolint
ENTRYPOINT ["python3", "-m", "codestyle"]
