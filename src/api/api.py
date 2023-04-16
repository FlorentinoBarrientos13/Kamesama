import requests
from api.types.user import UserInformation
from api import db
from dotenv import load_dotenv

API_ENDPOINT = "https://api.wanikani.com/v2"
REVISION = "20170710"

def is_valid_api_key(key:str):
    headers = {"Wanikani-Revision":REVISION,"Authorization":f"Bearer {key}"}
    response = requests.get(f"{API_ENDPOINT}/user",headers=headers)
    return response.status_code == 200


def get_request_headers_for_user(user:str, testing=False):
    key = load_dotenv("TEST_API_TOKEN") if testing else db.get_user_api_key(user)
    return {"Wanikani-Revision":REVISION,"Authorization":f"Bearer {key}"}

def get_number_of_reviews_and_lessons(user:str):
    pass

def request_user_information(user:str)-> UserInformation:
    headers = get_request_headers_for_user(user)
    response = requests.get(f"{API_ENDPOINT}/user",headers=headers)
    if (response.status_code == 200):
        user_data = response.json()
        return UserInformation(user_data)
    return None

def get_user_streaks(user:str):
    headers = get_request_headers_for_user(user)
    response = requests.get(f"{API_ENDPOINT}/reviews",headers=headers)
    if (response.status_code == 200):
        print(response.json())
    
    