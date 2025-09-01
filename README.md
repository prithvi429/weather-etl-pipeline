
# 🌦️ Weather ETL Pipeline

![Airflow](https://img.shields.io/badge/Airflow-2.0+-blue?logo=apacheairflow)
![Postgres](https://img.shields.io/badge/Postgres-13+-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)

## Overview

Weather ETL Pipeline is a robust, production-ready system for extracting real-time and historical weather data, transforming it, and loading it into a PostgreSQL database for analytics and visualization. Built with Apache Airflow, Docker, and Postgres.

---

## 🚀 Features
- Extracts weather data from Open-Meteo API
- Transforms and cleans data for analysis
- Loads data into a Postgres database
- Modular Airflow DAGs for easy scheduling
- Dockerized for easy deployment

---

## 🏗️ Architecture

```
┌────────────┐     ┌─────────────┐     ┌─────────────┐
│  Open-Meteo│ →  │ Airflow DAG │ →  │ Postgres DB │
└────────────┘     └─────────────┘     └─────────────┘
```

---

## 🛠️ Technologies Used
- Apache Airflow
- Docker & Docker Compose
- PostgreSQL
- Python

---

## ⚡ Quickstart

1. **Clone the repo:**
	```powershell
	git clone https://github.com/prithvi429/weather-etl-pipeline.git
	cd weather-etl-pipeline
	```
2. **Start services with Docker Compose:**
	```powershell
	docker-compose up --build
	```
3. **Access Airflow UI:**
	- Open [http://localhost:8080](http://localhost:8080)
	- Default credentials: `airflow` / `airflow`

---

## 📋 Usage

1. Configure your Airflow connections for Postgres and Open-Meteo API.
2. Trigger the DAG `etl_weather_dag` from the Airflow UI or set a schedule.
3. Data will be loaded into the `weather_data` table in Postgres.

---

## 📂 Folder Structure

```
weather-etl-pipeline/
├── dags/
│   └── etlwether.py
├── tests/
│   └── dags/
│       └── test_dag_example.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📝 DAG Overview

The main DAG (`etlwether.py`) performs:
- **Extract:** Fetches weather data from Open-Meteo API
- **Transform:** Cleans and structures the data
- **Load:** Inserts data into Postgres

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.
