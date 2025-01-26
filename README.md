# Weather real-time pipeline

## Introduction

Weather pipeline, extracting temperature data from Astronomical Site Monitoring (ASM) of European Sourthen Observatory (ESO) using Docker, docker-compose or Kubernetes, Python, InfluxDB, Apache Kafka and grafana.

API: <https://www.eso.org/sci/facilities/paranal/astroclimate/ASMDatabase/apicalls.html>

This project uses Docker and Docker Compose to deploy the entire application. It also includes a deploy folder containing YAML files or manifests for deploying the app using Kubernetes as an orchestrator.

The application consists of a Python app that retrieves data from the ASM ESO API. This API provides several endpoints with meteorological information for sites where astronomical observatories are located, such as the Paranal Observatory. The Python app queries the API and sends the data to an Apache Kafka cluster, which has a topic named weather_db. Additionally, the app deploys a time-series database, InfluxDB, using its data collection system, Telegraf. Telegraf consumes data from the Kafka cluster and writes it to InfluxDB. Finally, InfluxDB is connected to a Grafana instance, where a dashboard displays the data as a time-series chart.

![Figure 1](/images/docker_arch.png "Docker container based architecture")

## How to use

Firts, it is necessary to configure telegraf.config, you can use telegraf.config.sample file in the root of the project as a reference (mantain the new file in the same place). Also, is necessary to add a token value from InfluxDB at datasource.yml using datasource.yml.sample file as reference.

then just run docker-compose manifest with:

```bash
docker-compose build myapp
```
