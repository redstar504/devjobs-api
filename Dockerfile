FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi --no-dev

COPY . /app/

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
#CMD ["tail", "-f", "/dev/null"]