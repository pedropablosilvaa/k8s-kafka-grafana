from api_fetcher import WeatherAPI
from kafka_producer import KafkaProducerService
from kafka_consumer import KafkaConsumerService
#from grafana_publisher import send_to_grafana
from datetime import datetime, timedelta
from grafana_client import GrafanaApi

def main():

    # Definir el formato de tiempo y la URL de la API
    KAFKA_SERVER = 'broker:9092' 
    TOPIC = 'weather_topic'  # Topic name in Kafka
    current_time = datetime.today()
    end_time = current_time - timedelta(hours=1)
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S').replace(" ","T")
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S').replace(" ","T")
    URL_API = f'https://www.eso.org/asm/api/?from={end_time_str}Z&to={current_time_str}Z&fields=meteo_paranal-temp1'
    URL_GRAFANA = GrafanaApi("http://localhost:3000/")

    weather_api = WeatherAPI(api_url=URL_API)
    weather_data = weather_api.fetch_weather_data()

    # Create an instance of the KafkaProducerService
    kafka_service = KafkaProducerService(KAFKA_SERVER)
    kafka_service.send_to_kafka(TOPIC, weather_data)
    
    # Create an instance of the KafkaConsumerService
    kafka_consumer_service = KafkaConsumerService(KAFKA_SERVER, TOPIC)
    
    # Start consuming messages from Kafka
    kafka_consumer_service.consume_from_kafka()
    
    # fetch data from kafka and send it to grafana
    #for message in consume_from_kafka("weather_topic", kafka_server):
    #    # Paso 4: Procesar los datos (si es necesario)
    #    # Aquí puedes aplicar alguna lógica de procesamiento
    #    send_to_grafana(grafana_url, message)

if __name__ == "__main__":
    main()