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

FLIGHT_API_KEY = os.environ.get("FLIGHT_API_KEY")

@tool
def get_airport_id(AirportName: str) -> str:
    """ A tool that allows you to get the Airport ID"""

    url = f'https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination'

    headers = {
        "X-RapidAPI-Key": FLIGHT_API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    querystring = {"query": AirportName}

    response = requests.get(url, params={"key": FLIGHT_API_KEY}, headers=headers, querystring=querystring).json()

    print(response.json())


tools = [get_airport_id("Detroit")]
