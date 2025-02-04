FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask prometheus_client gunicorn

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz && \
    tar xvf prometheus-2.45.0.linux-amd64.tar.gz && \
    mv prometheus-2.45.0.linux-amd64/prometheus /usr/local/bin/ && \
    mv prometheus-2.45.0.linux-amd64/promtool /usr/local/bin/ && \
    rm -rf prometheus-2.45.0.linux-amd64*

RUN wget https://dl.grafana.com/oss/release/grafana-9.2.2.linux-amd64.tar.gz && \
    tar -zxvf grafana-9.2.2.linux-amd64.tar.gz && \
    mv grafana-9.2.2 /usr/local/grafana && \
    rm -rf grafana-9.2.2.linux-amd64.tar.gz

ENV GF_PATHS_HOME=/usr/local/grafana
ENV GF_PATHS_CONFIG=/usr/local/grafana/conf/defaults.ini
ENV GF_PATHS_DATA=/usr/local/grafana/data
ENV GF_PATHS_LOGS=/usr/local/grafana/logs
ENV GF_PATHS_PLUGINS=/usr/local/grafana/plugins

EXPOSE 5000 9090 3000

COPY prometheus.yml /etc/prometheus/prometheus.yml

CMD ["sh", "-c", "prometheus --config.file=/etc/prometheus/prometheus.yml & /usr/local/grafana/bin/grafana-server --homepath=/usr/local/grafana & gunicorn -w 4 -b 0.0.0.0:5000 server:app"]
