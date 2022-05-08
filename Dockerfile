# This is a simple Dockerfile to use while developing
# It's not suitable for production
FROM python:3.9.12-slim

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py ./
RUN pip install -r requirements.txt
RUN pip install -e .
COPY api api/
COPY migrations migrations/
ADD entrypoint.sh entrypoint.sh
RUN chmod u+x ./entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
