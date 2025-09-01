from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago

LATTITUDE = "51.5074"
LONGITUDE = "-0.1278"
POSTGRESS_CONN_ID = "postgres_localhost"
API_CONN_ID = "open_weather_api"

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id="etl_weather_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    @task()
    def extract_weather_data() -> dict:
        """Extract data from Open-Meteo API"""
        http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
        endpoint = f"/v1/forecast?latitude={LATTITUDE}&longitude={LONGITUDE}&current_weather=true"
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code}")

    @task()
    def transform_weather_data(weather_data: dict) -> dict:
        """Transform the extracted weather data"""
        current_weather = weather_data.get("current_weather")
        transformed_data = {
            "lattitude": LATTITUDE,
            "longitude": LONGITUDE,
            "temperature": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "winddirection": current_weather.get("winddirection"),
            "weathercode": current_weather.get("weathercode"),
        }
        return transformed_data

    @task()
    def load_weather_data(transformed_data: dict):
        """Load the transformed data into Postgres"""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRESS_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                lattitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode INT,
                observation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO weather_data (lattitude, longitude, temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['lattitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    # DAG Workflow
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)
