from kafka import KafkaConsumer
import json
from typing import Any

class KafkaConsumerService:
    """
    A class to consume messages from a Kafka topic.
    """

    def __init__(self, kafka_server: str, topic: str, group_id: str = "weather-consumer") -> None:
        """
        Initializes the Kafka consumer with the given parameters.
        
        :param kafka_server: The address of the Kafka server (e.g., 'localhost:9092')
        :param topic: The Kafka topic to consume messages from.
        :param group_id: The consumer group ID. Default is 'weather-consumer'.
        """
        self.kafka_server = kafka_server
        self.topic = topic
        #self.group_id = group_id
        
        # Initialize the Kafka consumer with the specified parameters
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.kafka_server,
            #group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize message as JSON
        )

    def consume_from_kafka(self) -> None:
        """
        Starts consuming messages from the specified Kafka topic.
        This method will run indefinitely, processing messages as they come in.
        """
        for message in self.consumer:
            print(f"Consumed message: {message.value}")
            # Here you can process the data before sending it to Grafana or any other system.