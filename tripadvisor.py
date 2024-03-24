from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    model_name="gpt-3.5-turbo"
)

TRIPADVISOR_API_KEY = os.environ.get("TRIPADVISOR_API_KEY")

@tool
def get_nearby_attraction(latLong: str) -> str:
    """A tool that allows you to get attractions close to a given lattitude and longitude pair. The input should just be a pair of floats that looks like this: 51.5074, -0.1278. Do not add any other text."""

    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"latLong": latLong, "key": TRIPADVISOR_API_KEY, "category":"attractions"}, headers=headers).json()
 
    return_string = ""
    for location in response['data']:
        return_string += f"Location ID: {location['location_id']}, Name: {location['name']}\n"
    return return_string

@tool
def get_nearby_hotel(latLong: str) -> str:
    """A tool that allows you to get hotels close to a given lattitude and longitude pair. The input should just be a pair of floats that looks like this: 51.5074, -0.1278. Do not add any other text."""

    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"latLong": latLong, "key": TRIPADVISOR_API_KEY, "category":"hotels"}, headers=headers).json()
 
    return_string = ""
    for location in response['data']:
        return_string += f"Location ID: {location['location_id']}, Name: {location['name']}\n"
    return return_string

@tool
def get_nearby_restaurants(latLong: str) -> str:
    """A tool that allows you to get restaurants close to a given lattitude and longitude pair. The input should just be a pair of floats that looks like this: 51.5074, -0.1278. Do not add any other text."""

    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"latLong": latLong, "key": TRIPADVISOR_API_KEY, "category":"restaurants"}, headers=headers).json()
 
    return_string = ""
    for location in response['data']:
        return_string += f"Location ID: {location['location_id']}, Name: {location['name']}\n"
    return return_string

@tool
def get_location_info(location_id: str) -> str:
    """A tool that returns information about a location. The input should be a location id number without extra information."""
    url = f'https://api.content.tripadvisor.com/api/v1/location/{location_id}/details'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"key": TRIPADVISOR_API_KEY}, headers=headers).json()
    return f"""
Name: {response.get("name", None)}
Description: {response.get("description", None)}
Phone: {response.get("phone", None)}
Website: {response.get("website", None)}
Rating: {response.get("rating", None)}
Price Level: {response.get("price_level", None)}
Hours:
Features: {response.get("features", None)}
Amenities: {response.get("amenities", None)}
"""

tools = [get_nearby_attraction, get_location_info, get_nearby_hotel, get_nearby_restaurants]

from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=40
)

if __name__ == "__main__":
    location = "Jersey City"
    zero_shot_agent(f"""Give me 3 hotels, 5 restaurants, and 5 attractions near {location}.
                    Your answer must include their names, descriptions, phone numbers, ratings, prices, and websites in list format.
                    Each answer must include a description and price.
                    Sort the answers by rating.""")
