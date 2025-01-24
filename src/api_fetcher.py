import requests
import json
from datetime import datetime
from typing import Dict


class WeatherAPI:
    """
    class to interact with weather API
    """

    def __init__(self, api_url: str) -> None:
        """
        Init class with URL API
        
        :param api_url: Full URL to get query API
        """
        self.api_url = api_url

    def fetch_weather_data(self) -> Dict:
        """
        Query the API and fetch data
        
        :return: Dict with data obteined or void dict in error case.
        """
        try:
            response_api = requests.get(self.api_url)
            print(f'get data status code: {response_api.status_code}')
            response_api.raise_for_status()  # error
            data = response_api.text
            parsed_data = json.loads(data)
            #print(parsed_data)  # show data fetched from API
            return parsed_data
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
