FROM python:2.7.14

WORKDIR /home

# AWS KEYS
ENV ACCES_KEY=AKIAJQND64KSHJ265EMA 
ENV SECRET_KEY=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
ENV BUCKET_NAME=course-election-repository

# DEPENDENCIES
RUN pip install boto3