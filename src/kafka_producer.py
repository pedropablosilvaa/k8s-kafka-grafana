from kafka import KafkaProducer
import json
from typing import Dict
import time

class KafkaProducerService:
    """
    A class to send data to a Kafka topic.
    """

    def __init__(self, kafka_server:str) -> None:
        """
        Initializes the Kafka producer with the given Kafka server address.
        
        :param kafka_server: The address of the Kafka server (e.g., 'localhost:9092')
        """
        self.kafka_server = kafka_server
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_server  # Serialize the data to JSON and encode it as UTF-8
        )

    def send_to_kafka(self, topic: str, data: dict) -> None:
        """
        Sends data to a specified Kafka topic.
        
        :param topic: The Kafka topic to send the data to.
        :param data: The data to send, in the form of a dictionary.
        """
        # send data to a specific topic
        self.producer.send(topic, data)
        # Flush the producer to ensure all messages are sent
        self.producer.flush()

        print(f"Data sent to Kafka topic: {topic}")

