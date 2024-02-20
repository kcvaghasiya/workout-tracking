import requests
from datetime import datetime
import os

NUTRI_APP_ID = os.environ.get('nutri_app_id')
NUTRI_APP_KEY = os.environ.get('nutri_app_key')
NUTRI_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_PROJECT = "myWorkoutsTracking"
SHEETY_WORKSHEET = "workouts"
SHEETY_ENDPOINT = f"{os.environ.get('sheety_endpoint')}/{SHEETY_PROJECT}/{SHEETY_WORKSHEET}"


nutri_headers = {
    "x-app-id": NUTRI_APP_ID,
    "x-app-key": NUTRI_APP_KEY
}
query_text = input("Tell me which exercise you did: ")

nutri_params = {
    "query": query_text,
}
response = requests.post(NUTRI_URL, headers=nutri_headers, json=nutri_params)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
headers = {
    "Authorization": os.environ.get("sheety_authorization")
}
for exercise in result["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_input, headers=headers)
    print(sheet_response.text)
