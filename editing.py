import subprocess
import os
from utilities import whisperapi_audio, save_transcription_as_srt, convert_to_mp3

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

def video_text(input_file_path, text, social_media, font_size, font_color):

  file_name = os.path.basename(input_file_path)
  
  output_file = f"video-text/{file_name}"

  if social_media == "instagram":
    width, height = 1080, 1920
  if social_media == "youtube":
    width, height = 900, 1600

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

  command = [
      'ffmpeg',
      '-i', input_file_path,
      '-vf', f"drawtext=text='{text}':fontfile=/path/to/your/font.ttf:fontsize={font_size}:fontcolor={font_color}:x=(w-text_w)/2:y={height/4}",
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

#if video_ratio("video-raw/ferenc-puskas-110478.mp4", "video-ratio/ratio-ferenc-puskas-110478.mp4", "instagram"):
#  video_text("video-ratio/ratio-ferenc-puskas-110478.mp4", "video-text/text-ferenc-puskas-110478.mp4", "Placeholder1 vs Placeholder2", "instagram", 48, "white")

def video_transcribe(input_file_path, quality=128, local=False, model=False):
    
    file_name = os.path.basename(input_file_path)
  
    output_file = f"video-subtitles/{file_name}"

    language = False
    prompt = "focus on natural speech"

    if input_file_path.lower().endswith(".mp4"):
        audio_file = convert_to_mp3(input_file_path, quality)
        
    audio_path = os.path.splitext(audio_file)[0]

    try:
        if local == "1":
            #local_whisper(file_path, model, language, prompt) this function is commented out in utilities.py file
            pass # ! change if convertation to local model is needed
        else:
            transcription = whisperapi_audio(audio_file, language, prompt)
            subtitle_path = save_transcription_as_srt(transcription, audio_path, language)

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

def edit_video(input_file, social_media):
  output_ratio_file = video_ratio(input_file, social_media)
  output_text_file = video_text(output_ratio_file, "Placeholder 1 vs Placeholder 2", social_media, 48, "white")
  subtitle_path = video_transcribe(output_text_file, quality=128, local=False, model=False)
  output_final_file = add_subtitles_to_video(output_text_file, subtitle_path, 12)

  return output_final_file

edit_video("video-raw/rivaldo-vitor-borba-ferreira-4239.mp4", "instagram")
   

# Example usage:
#video_name = "rivaldo-vitor-borba-ferreira-4239.mp4"
#input_video = 'video-raw/rivaldo-vitor-borba-ferreira-4239.mp4'
#output_audio = 'video-subtitles/audio-rivaldo-vitor-borba-ferreira-4239.mp3'
#credentials_path = 'assets/high-ace-449308-i2-df5a2e758333.json' 
#output_srt = 'video-subtitles/rivaldo-vitor-borba-ferreira-4239.en.srt'
#output_video_with_subtitles = 'video-final/final-rivaldo-vitor-borba-ferreira-4239.mp4'

#extract_audio(input_video, output_audio)
#transcripts, detected_language = transcribe_audio_auto_language(output_audio, credentials_path)
#create_srt_file(transcripts, output_srt)
#add_subtitles_to_video(input_video, output_srt, output_video_with_subtitles)

#print(f"Detected language: {detected_language}")