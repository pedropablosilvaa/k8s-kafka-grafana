import requests
from typing import Dict

class GrafanaClient:
    def __init__(self, grafana_url: str):
        self.grafana_url = grafana_url

    def send_to_grafana(self, data: Dict[str, any]) -> None:
        """Send data to Grafana"""
        try:
            response = requests.post(self.grafana_url, json=data)
            response.raise_for_status()
            print(f"Data sent to Grafana: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending data to Grafana: {e}")

# Usage example:
# grafana = GrafanaClient("http://your-grafana-url")
# grafana.send_to_grafana({"key": "value"})
