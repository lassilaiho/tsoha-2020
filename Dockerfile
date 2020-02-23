FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip3 install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile
EXPOSE 5000
CMD python3 ./run.py
COPY . .
