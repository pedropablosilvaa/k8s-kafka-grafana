from api_fetcher import WeatherAPI
from kafka_producer import KafkaProducerService
#from kafka_consumer import KafkaConsumerService
#from grafana_publisher import send_to_grafana
from datetime import datetime, timedelta
from grafana_client import GrafanaApi
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json

KAFKA_SERVER = 'broker:9092' 
TOPIC = 'weather_topic'  # Topic name in Kafka

def fetch_and_produce():
    # Definir el formato de tiempo y la URL de la API
    current_time = datetime.today()
    end_time = current_time - timedelta(hours=1)
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S').replace(" ","T")
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S').replace(" ","T")
    URL_API = f'https://www.eso.org/asm/api/?from={end_time_str}Z&to={current_time_str}Z&fields=meteo_paranal-temp1'
    
    weather_api = WeatherAPI(api_url=URL_API)
    weather_data = weather_api.fetch_weather_data()
    latest_data = list(weather_data["meteo_paranal-temp1"])[-1]
    # Convert Unix timestamp to date
    unix_timestamp_ms = latest_data[0]
    unix_timestamp_seconds = unix_timestamp_ms / 1000
    date = datetime.fromtimestamp(unix_timestamp_seconds)
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

    # Create JSON object
    json_data = {
        "timestamp": formatted_date,  # Human-readable date
        "temperature": latest_data[1]        # Temperature value
    }

    # Convert to JSON string
    json_string = json.dumps(json_data).encode('utf-8')


    kafka_service = KafkaProducerService(KAFKA_SERVER)
    kafka_service.send_to_kafka(TOPIC, json_string)
    print(f"Weather data produced to Kafka at {current_time_str}") 
    print(f"Data ingest in kafka: {json_string}")  


#def consume_and_send_to_grafana():
#   kafka_consumer_service = KafkaConsumerService(KAFKA_SERVER, TOPIC)
#    
#    # Aquí consumimos los mensajes de Kafka y los enviamos a Grafana
#    kafka_consumer_service.consume_from_kafka()
#    print("Data consumed from Kafka and sent to Grafana")


def main():
    scheduler = BackgroundScheduler()

    # Configurar los trabajos para que se ejecuten cada minuto
    scheduler.add_job(fetch_and_produce, 'interval', minutes=1)
    #scheduler.add_job(consume_and_send_to_grafana, 'interval', minutes=1)
    
    scheduler.start()

    try:
        # Mantener el programa corriendo para que el scheduler ejecute los trabajos
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    
if __name__ == "__main__":
    main()