from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    model_name="gpt-3.5-turbo"
)

#Unused
FLIGHT_API_KEY = os.environ.get("FLIGHT_API_KEY")

@tool
def get_airport_id(AirportName: str) -> str:
    """ A tool that allows you to get the Airport ID"""

    url = f'https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination'

    # hardcode API key to test until we fix env
    headers = {
        "X-RapidAPI-Key": '0a7f525df1msh13de0e4eb342e73p14f087jsn16769e4c2a11',
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    querystring = {"query": AirportName}

    response = requests.get(url, headers=headers, params=querystring).json()

    print(response)
    return_string = ""
    for location in response['data']:
        return_string += f"Airport ID: {location['id']}\n"
    return return_string



@tool
def getFlightToken(Airport1ID: str, Airport2ID: str, DepartureDate: str, ReturnDate: str, Adults: int, Children: str) -> str:
    """ A tool that allows you to get the token for the flight between two airports"""

    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

    querystring = {"fromId":f"{Airport1ID}","toId":f"{Airport2ID}","departDate":f"{DepartureDate}", "returnDate":f"{ReturnDate}","pageNo":"1","adults":f"{Adults}","children":f"{Children}","currency_code":"USD"}


    headers = {
        "X-RapidAPI-Key": "07f525df1msh13de0e4eb342e73p14f087jsn16769e4c2a11",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())

    return_string = ""
    for token in response['data']:
        return_string += f"Token: {token['flightOffers']}"
    return return_string


# tools = [get_airport_id("Detroit"), getFlightToken("DTT.CITY", "ATL.AIRPORT", "2024-04-03", "2024-04-11", 1, 2)]
getFlightToken("DTT.CITY", "ATL.AIRPORT", "2024-04-03", "2024-04-11", 1, "0,1,17")