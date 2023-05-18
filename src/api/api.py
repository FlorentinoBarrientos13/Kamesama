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

def calculate_user_streaks(data):

    return data

def get_user_streaks(user:str):
    headers = get_request_headers_for_user(user)
    #just get all the responses
    response = requests.get(f"{API_ENDPOINT}/assignments?updated_after=2000-04-20T18:15:47",headers=headers)
    if (response.status_code == 200):
        first_data = response.json()
        cached = db.has_cached_streak(user)
        last_updated_date = None
        if cached != None:
            last_updated_date = cached['data_updated_at']
        
        if last_updated_date != None and  last_updated_date == first_data['data_updated_at']:
            return calculate_user_streaks(first_data)
        else:
            date = first_data['pages']['next_url']
            while date != None:
                new_request = requests.get(date,headers=headers)
                data = new_request.json()
                first_data['data'].append(data['data'])
                date = data['pages']['next_url']
            db.cache_streak(user,data)

        
        return calculate_user_streaks(data)



def get_user_available_reviews_and_lessons(user:str):
    headers = get_request_headers_for_user(user)
    response = requests.get(f"{API_ENDPOINT}/summary",headers=headers)
    review_count = 0
    lesson_count = 0
    if (response.status_code == 200):
        response_json = response.json()
        reviews = response_json['data']['reviews']
        lessons = response_json['data']['lessons']
        for review in reviews:
             review_count += len(review['subject_ids'])
        for lesson in lessons:
             lesson_count += len(lesson['subject_ids'])
    return review_count,lesson_count

    
def get_server_levels_leaderboard():
    users = db.get_registered_users()
    profiles = list(map(lambda x : request_user_information(x),users))
    profiles.sort(reverse=True, key=lambda x : x.level)
    return profiles
