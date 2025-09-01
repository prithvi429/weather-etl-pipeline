from airflow import DAG
from airflow.providers.https.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago



# latitude and longitude for London
LATTITUDE = "51.5074"
LONGITUDE  = "-0.1278"
POSTGRESS_CONN_ID = "postgres_localhost"
API_CONN_ID = "open_weather_api"


default_args = {
    'owner': 'airflow', 
    'start_date': days_ago(1),
    
    }


#DAG

with DAG(
    dag_id = "etl_weather_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    @task()
    def extract():
        """Extract data from OpenWeather API"""
        http = HttpHook(method='GET', http_conn_id=API_CONN_ID)
        endpoint = f"data/2.5/weather?lat={LATTITUDE}&lon={LONGITUDE}&appid=YOUR_API_KEY&units=metric"
        response = http.run(endpoint)
        data = response.json()
        return data

    @task()
    def transform(data: dict):
        """Transform the extracted data"""
        transformed_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description']
        }
        return transformed_data

    @task()
    def load(data: dict):
        """Load the transformed data into Postgres"""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRESS_CONN_ID)
        insert_query = """
            INSERT INTO weather (city, temperature, humidity, weather_description)
            VALUES (%s, %s, %s, %s)
        """
        pg_hook.run(insert_query, parameters=(data['city'], data['temperature'], data['humidity'], data['weather_description']))

    # Define task dependencies
    raw_data = extract()
    transformed_data = transform