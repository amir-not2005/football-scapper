import requests
from constants import COOKIES, HEADERS, BASE_URL


'''
Fetches video data using get requests to obtain json response:
[
    {
        "mediaid": 110478,
        "image": "/cache/matches/82bc0f3377aa4d65603729c29e154d99.png",
        "title": "Germany vs. Hungary",
        "description": "July 04, 1954",
        "file": "/uploads/goal/source_file/110478/ferenc-puskas-110478.mp4"
    }
    {...}
]

Returns a list of videos of same competition with description:
[
    {
        "competition_title": "World Cup 1954"
        "teams": ["Germany", "Hungary"],
        "date": "July 04, 1954",
        "file": "/uploads/goal/source_file/110478/ferenc-puskas-110478.mp4"
    }
    {...}
]

'''
def fetch_competition_vids(competition_id, page):
    
    # Parameters to fetch json 
    params = {
        'player_id': '',
        'competition_id': competition_id,
        'team_id': '',
        'team_ids': '',
        'page': page
    }

    request = requests.request("GET", BASE_URL, params=params)
    json_data = request.json()
    
    return json_data # Not finished yet

print(fetch_competition_vids(4, 1))
