from editing import edit_video
from scrapper import download_vid, fetch_competition_vids, create_video_description
from constants import COMPETITION_TITLE

videos_json = fetch_competition_vids(COMPETITION_TITLE['World Cup'], 19)
social_media = "instagram" #change if needed

for i in range(1): # run for 5 fetched videos
    video_json = videos_json[i]
    video_description = create_video_description(video_json)
    downloaded_video_path = download_vid(video_description['path'])
    output_final_file = edit_video(downloaded_video_path, social_media, video_description)

print(f"\033[92mFinished working with {i+1} videos\033[0m")