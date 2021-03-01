FROM python:3.8.1-buster
RUN apt-get update && apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    pip install --upgrade pip

COPY / /app
WORKDIR /app
RUN pip install --disable-pip-version-check -r /app/requirements.txt && \
    pip install .

ENTRYPOINT ["python", "-m", "src"]
