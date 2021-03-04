FROM python:3.8.1-buster

WORKDIR /

RUN apt-get update && \
    apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev wget && \
    pip install --upgrade pip

RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.1.1/node_exporter-1.1.1.linux-arm64.tar.gz && \
    tar xvfz node_exporter-1.1.1.linux-arm64.tar.gz && \
    useradd -M -r -s /bin/false node_exporter && \
    cp node_exporter-1.1.1.linux-arm64/node_exporter /usr/local/bin/ && \
    chown node_exporter:node_exporter /usr/local/bin/node_exporter

COPY app /app

WORKDIR /app
RUN pip install --disable-pip-version-check -r requirements.txt && \
    pip install .

WORKDIR /app
ENTRYPOINT ["python", "-m", "src"]
