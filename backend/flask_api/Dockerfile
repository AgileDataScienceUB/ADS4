FROM python:3.6.3

# AWS KEYS
ENV AWS_ACCES_KEY_ID=AKIAJQND64KSHJ265EMA
ENV AWS_SECRET_ACCES_KEY=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
ENV BUCKET_NAME=course-election-repository

WORKDIR /usr/src/site/code

COPY requirements.txt /opt/

RUN pip install -r /opt/requirements.txt

ENV APP_SETTINGS=/usr/src/site/code/etc/defaults.cfg
