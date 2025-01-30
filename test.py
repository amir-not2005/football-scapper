import requests
from constants import BASE_URL


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

    request = requests.request("GET", BASE_URL+"/goals", params=params)
    json_data = request.json()
    
    return json_data['goals'] # Not finished yet


'''
Save video to "video-raw/rivaldo-vitor-borba-ferreira-4239.mp4" based on the URL of the video:

"https://footballia.eu/uploads/goal/source_file/8147/diego-martin-forlan-corazo-8147.mp4"

by get request

'''

def download_vid(file_path):
    print(BASE_URL+file_path)
    request = requests.request("GET", BASE_URL+file_path, stream=True)
    
    if request.status_code == 200:
        file_name = file_path.split("/")[-1]
        with open("video-raw/"+file_name, "wb") as f:
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video {file_name} downloaded ")

    else:
        print(f"Failed to download video {file_name}")

#download_vid(fetch_competition_vids(COMPETITION_TITLE["World Cup"], 13)[0]["file"])