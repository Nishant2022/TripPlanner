from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

FLIGHT_API_KEY = os.environ.get("FLIGHT_API_KEY")

@tool
def get_airport_id(AirportName: str) -> str:
    """ A tool that allows you to get the Airport ID. Input should be a city name."""

    url = f'https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination'

    headers = {
        "X-RapidAPI-Key": FLIGHT_API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    querystring = {"query": AirportName}

    response = requests.get(url, headers=headers, params=querystring).json()

    return_string = ""
    for location in response.get('data', []):
        if location.get('type') == 'AIRPORT':
            return_string += f"Airport ID: {location['id']}\n"
    return return_string


@tool
def getFlightToken(input_string: str) -> str:
    """ A tool that allows you to get the token for the flight between two airports.
        The input should be in the following format:
        DepartureAirportID:ArrivalAirportID:DepartureDate:ReturnDate:NumAdults
        
        The dates should be in YYYY-MM-DD format. The year is 2024.
    """

    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

    print(input_string)
    
    Airport1ID, Airport2ID, DepartureDate, ReturnDate, Adults = input_string.split(':')
    print(Airport1ID, Airport2ID, DepartureDate, ReturnDate, Adults)

    querystring = {
        "fromId": Airport1ID, 
        "toId": Airport2ID, 
        "departDate": DepartureDate,
        "returnDate": ReturnDate,
        "pageNo": "1",
        "adults": Adults,
        "currency_code": "USD"
        }
    
    headers = {
        "X-RapidAPI-Key": FLIGHT_API_KEY,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    print(response)

    return_string = ""
    for flight in response['data']['flightDeals']:
        return_string += f"Type: {flight['key']}, Token: {flight['offerToken']}\n"
    return return_string

if __name__ == "__main__":
    from langchain.agents import initialize_agent
    
    tools = [get_airport_id, getFlightToken]
    
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
        model_name="gpt-3.5-turbo"
    )
    
    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=40
    )
    
    zero_shot_agent("Find me the cheapest flight from New York to LA departing on April 15 and returning on April 20")