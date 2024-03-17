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

@tool
def get_nearby(latLong: str) -> str:
    """A tool that allows you to get attractions and restaurants close to a given lattitude and longitude pair. The input should just be a pair of floats without parentheses or extra info."""
    
    url = f'https://api.content.tripadvisor.com/api/v1/location/nearby_search?key={os.environ.get("TRIPADVISOR_API_KEY")}'

    headers = {"accept": "application/json"}

    response = requests.get(url, params={"latLong": latLong}, headers=headers).json()
    
    return_string = ""
    for location in response['data']:
        return_string += f"Location ID: {location['location_id']}, Name: {location['name']}\n"
    return return_string
    
tools = [get_nearby]

from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3
)

if __name__ == "__main__":
    zero_shot_agent("What are some locations near London?")