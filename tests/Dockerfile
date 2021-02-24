FROM php:7.4.10-cli-alpine3.12
WORKDIR /app
RUN apk add --no-cache \
        bzip2-dev coreutils dpkg-dev dpkg expat-dev findutils gcc gdbm-dev libc-dev libffi-dev libnsl-dev libtirpc-dev \
        linux-headers make ncurses-dev openssl-dev pax-utils readline-dev sqlite-dev tcl-dev tk tk-dev util-linux-dev \
        xz-dev zlib-dev yaml-dev git curl bash npm=12.21.0-r0 \
    && curl https://pyenv.run | bash
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN pyenv install 3.6.12 && pyenv install 3.7.9 && pyenv install 3.8.6 && pyenv install 3.9.0 \
    && pyenv global 3.6.12 3.7.9 3.8.6 3.9.0  \
    && python3 -m pip --no-cache-dir install --upgrade pip \
    && python3 -m pip --no-cache-dir install tox==3.20.0 PyYAML==5.3.1 \
    && pear install --soft --onlyreqdeps PHP_CodeSniffer-3.5.6 \
    && apk add shellcheck
COPY . .
RUN npm install \
    && rm -r /tmp/*
ENV PATH /app/node_modules/.bin/:$PATH
CMD ["python", "-m", "tox"]
