FROM postgres:14

RUN apt-get update && apt-get install -y \
    postgresql-server-dev-14 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --branch v0.4.0 https://github.com/pgvector/pgvector.git /usr/src/pgvector \
    && cd /usr/src/pgvector \
    && make \
    && make install
