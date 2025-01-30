import subprocess
import os
from transcribe_utilities import whisperapi_audio, save_transcription_as_srt, convert_to_mp3

def video_ratio(input_file_path, social_media):
  """
  Adds black padding to the input video to match the desired aspect ratio.

  Args:
    input_file: Path to the input MP4 video file.
    output_file: Path to the output MP4 video file.
    social_media: Defines width and height fitting specific social media
  """

  file_name = os.path.basename(input_file_path)
  
  output_file = f"video-ratio/{file_name}"

  if social_media == "instagram":
    width, height = 1080, 1920
  if social_media == "youtube":
    width, height = 900, 1600

  command = [
      'ffmpeg',
      '-i', input_file_path, 
      '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1', 
      '-c:v', 'libx264', 
      '-c:a', 'copy', 
      output_file
  ]

  try:
    subprocess.run(command, check=True)
    print(f"Successfully created {output_file}")
    return output_file
  except subprocess.CalledProcessError as e:
    print(f"Error processing video: {e}")
    return False

def video_text(input_file_path, video_description, social_media, font_size, font_color):

  file_name = os.path.basename(input_file_path)
  output_file = f"video-text/{file_name}"

  if social_media == "instagram":
    width, height = 1080, 1920
  if social_media == "youtube":
    width, height = 900, 1600

  font_path = "assets/Zain-Light.ttf"
  padding = 10
  text_teams = video_description['teams']
  text_scorer = video_description['scorer']
  text_date = video_description['date']

  """
  Adds text overlay to the input video.

  Args:
    input_file: Path to the input MP4 video file.
    output_file: Path to the output MP4 video file.
    text: Text to be added to the video.
    x: X-coordinate for text placement. (based on width)
    y: Y-coordinate for text placement. (based on height)
    font_size: Font size for the text.
    font_color: Color of the text (e.g., 'white', 'red', 'black').
  """

  y_team = padding + height/8  # Teams
  y_date = y_team + font_size + padding  # Date
  y_scorer = y_date + font_size + padding  # Scorer

  command = [
      'ffmpeg',
      '-i', input_file_path,
      '-vf',
      f"""
      drawtext=
          text='{text_teams}':
          fontfile='{font_path}':
          fontsize={font_size}:
          fontcolor={font_color}:
          x=(w-text_w)/2:
          y={y_team},
      drawtext=
          text='{text_date}':
          fontfile='{font_path}':
          fontsize={font_size}:
          fontcolor={font_color}:
          x=(w-text_w)/2:
          y={y_date},
      drawtext=
          text='{text_scorer}':
          fontfile='{font_path}':
          fontsize={font_size}:
          fontcolor={font_color}:
          x=(w-text_w)/2:
          y={y_scorer}
      """,  # Multi-line -vf for readability
      '-c:v', 'libx264',
      '-c:a', 'copy',
      output_file
  ]

  try:
    subprocess.run(command, check=True)
    print(f"Successfully added text to {output_file}")
    return output_file
  except subprocess.CalledProcessError as e:
    print(f"Error adding text to video: {e}")
    return False

def video_transcribe(input_file_path, quality=128, local=False, model=False):
    
    file_name = os.path.basename(input_file_path)
  
    output_file = f"video-subtitles/{file_name}"

    prompt = "focus on natural speech"

    if input_file_path.lower().endswith(".mp4"):
        audio_file = convert_to_mp3(input_file_path, quality)
        
    audio_path = os.path.splitext(audio_file)[0]

    try:
        if local == "1":
            #local_whisper(file_path, model, language, prompt) this function is commented out in utilities.py file
            pass # ! change if convertation to local model is needed
        else:
            transcription = whisperapi_audio(audio_file, prompt)
            subtitle_path = save_transcription_as_srt(transcription, audio_path)

        print("Transcription complete. Srt file saved.")

        return subtitle_path
    except Exception as e:
        print("Error", f"An error occurred during transcription: {e}")
    
    

def add_subtitles_to_video(input_video_path, subtitles_file, font_size):

  file_name = os.path.basename(input_video_path)
  
  output_file = f"video-final/{file_name}"

  """
  Adds subtitles to the input video.

  Args:
    input_video: Path to the input video file.
    subtitles_file: Path to the SRT subtitle file.
    output_video: Path to the output video file.
  """

  command = [
      'ffmpeg',
      '-i', input_video_path,
      '-vf', f"subtitles={subtitles_file}:force_style='FontSize={font_size}'",  # Add FontSize
      '-c:v', 'libx264',
      '-c:a', 'copy',
      output_file
  ]

  try:
    subprocess.run(command, check=True)
    print(f"Successfully added subtitles to {output_file}")
  except subprocess.CalledProcessError as e:
    print(f"Error adding subtitles to video: {e}")
  
  return output_file

def edit_video(input_file, social_media, video_description):  
  output_ratio_file = video_ratio(input_file, social_media)
  output_text_file = video_text(output_ratio_file, video_description, social_media, 48, "white")
  subtitle_path = video_transcribe(output_text_file, quality=128, local=False, model=False)
  output_final_file = add_subtitles_to_video(output_text_file, subtitle_path, 12)

  return output_final_file