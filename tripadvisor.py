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
def get_nearby(latLong: str) -> str:
    """A tool that allows you to get attractions and restaurants close to a given lattitude and longitude pair. The input should just be a pair of floats that looks like this: 51.5074, -0.1278. Do not add any other text."""

    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search'

    headers = {"accept": "application/json"}

    print(f'LatLong provided: {latLong}')
    response = requests.get(url, params={"latLong": latLong, "key": TRIPADVISOR_API_KEY}, headers=headers).json()
 
    return_string = ""
    print(response)
    for location in response['data']:
        return_string += f"Location ID: {location['location_id']}, Name: {location['name']}\n"
    return return_string

@tool
def get_location_info(location_id: str) -> str:
    """A tool that returns information about a location. The input should be a location id string"""
    url = f'https://api.content.tripadvisor.com/api/v1/location/{location_id}/details'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"key": TRIPADVISOR_API_KEY}, headers=headers).json()
    print(response)
    return f"""
Name: {response["name"]}
Description: {response["description"]}
Phone: {response["phone"]}
Website: {response["website"]}
Rating: {response["rating"]}
Price Level: {response["price_level"]}
Hours:
Features: {response["features"]}
"""

tools = [get_nearby, get_location_info]

from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3
)

if __name__ == "__main__":
    # print(get_location_info("2361377"))
    zero_shot_agent("What are some locations near Paris and give me more information about them?")
