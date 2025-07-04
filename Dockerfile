FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.3
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


COPY . .

RUN chmod +x entrypoint.sh

CMD ["bash", "entrypoint.sh"]
