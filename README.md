# Monitoring-Alerting-with-Prometheus-Grafana-and-AI

## Installation

1. Install Prometheus, Grafana, and Node Exporter.
2. Access them at their respective ports.

## Create a Dashboard in Grafana

1. Set up a new dashboard in Grafana.

## Retrieve CPU Usage Data

1. Use the following `curl` command to retrieve `cpu_usage.json` content:

    ```sh
    curl -G 'http://128.199.20.125:9090/api/v1/query_range' \
         --data-urlencode "query=100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)" \
         --data "start=$start" \
         --data "end=$end" \
         --data "step=15" > cpu_usage.json
    ```

## Training Dataset

1. The `cpu_usage.json` dataset will be used for training.

## Predict CPU Usage

1. Run the following command to predict CPU usage:

    ```sh
    python3 predictions.py
    ```

2. The `predictions.py` script will also create an HTTP server to store the metrics named `cpu_predictions`, which will be scraped by Prometheus.

## Alerting in Grafana

1. Once the above steps are completed, set up alerts in Grafana based on the `cpu_predictions` metrics.
