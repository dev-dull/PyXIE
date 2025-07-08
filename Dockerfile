FROM python:3-slim AS builder

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3-slim

ARG LISTEN_PORT=8000
ENV LISTEN_PORT=${LISTEN_PORT}

RUN mkdir /app
WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY ddb.py pyxie.py constfig.py config.yaml run.sh ./
ENV PATH=/root/.local/bin:$PATH

EXPOSE ${LISTEN_PORT}
CMD ["/app/run.sh"]
