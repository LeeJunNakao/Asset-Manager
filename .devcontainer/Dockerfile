FROM python:3.9.0
WORKDIR /home/app
EXPOSE 8000
ENV PYTHON_VERSION=3.9 \
  APP_PATH=/home/app \
  PATH=/home/python/.local/lib/python3.8/site-packages:/usr/local/bin:/home/python:/home/python/app/bin:$PATH:/usr/app:/root/.poetry/bin
RUN pip install -U pip
RUN pip install -U pytest
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version 1.1.8
RUN poetry config virtualenvs.create false
COPY pyproject.toml pyproject.toml
RUN poetry install
RUN pip install psycopg2-binary