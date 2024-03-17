import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_nearby(latLong: str):
    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search?key={os.environ.get("TRIPADVISOR_API_KEY")}'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"key": os.environ.get("TRIPADVISOR_API_KEY"), "latLong": latLong}, headers=headers)

    print(response.text)
    
if __name__ == "__main__":
    get_nearby("42.3455%2C-71.10767")