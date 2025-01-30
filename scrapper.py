import requests
from constants import BASE_URL
import os

'''
Fetches video data using get requests to obtain json response:

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
    
    # edit json data

    return json_data['goals'] # Not finished yet

'''
Takes json data of one video and parses it
'''

def create_video_description(video_json):
    path = video_json['file']
    teams = video_json['title']
    date = video_json['description']

    scorer_tmp = os.path.basename(video_json['file'])
    scorer_tmp = scorer_tmp.split("-")
    scorer = " ".join(scorer_tmp[:-1]).title()

    video_description = {
        "path": path,
        "teams": teams,
        "date": date,
        "scorer": scorer
    }

    return video_description
'''
Save video to "video-raw/rivaldo-vitor-borba-ferreira-4239.mp4" based on the URL of the video:

"https://footballia.eu/uploads/goal/source_file/8147/diego-martin-forlan-corazo-8147.mp4"

by get request

'''

def download_vid(file_path):
    print(f"Downloading file: {BASE_URL+file_path}")
    request = requests.request("GET", BASE_URL+file_path, stream=True)
    
    if request.status_code == 200:

        file_name = file_path.split("/")[-1]
        output_file = "video-raw/"+file_name

        with open(output_file, "wb") as f:
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video {file_name} downloaded ")
        
        return output_file
    else:
        print(f"Failed to download video {file_name}")