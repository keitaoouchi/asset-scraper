FROM python:3.7-alpine

RUN apk update && \
    apk add curl ttf-freefont chromium chromium-chromedriver build-base libffi-dev openssl-dev

# https://lifedevops.com/?p=173
# 日本語を処理できるように日本語フォントを導入
RUN mkdir /noto
ADD https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip /noto
WORKDIR /noto
RUN unzip NotoSansCJKjp-hinted.zip && \
    mkdir -p /usr/share/fonts/noto && \
    cp *.otf /usr/share/fonts/noto && \
    chmod 644 -R /usr/share/fonts/noto/ && \
    fc-cache -fv \
    rm -rf /noto

RUN mkdir /spider
ADD ./src /spider
WORKDIR /spider

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

CMD exec gunicorn --bind :8080 --workers 1 --threads 2 --chdir spider --graceful-timeout 300 app:app