import os
import subprocess
import shutil
import subprocess
from constants import API_KEY

api_key = API_KEY

def whisperapi_audio(audio_file, prompt):
    # This is needed because some video titles aren't parsed correctly by openAI.  Yields a "1"
    new_name = "transcribe.mp3"
    shutil.copy(audio_file, new_name)
    cmd = [
        "curl",
        "https://api.openai.com/v1/audio/transcriptions",
        "-X","POST",
        "-H",f"Authorization: Bearer {api_key}",
        "-H","Content-Type: multipart/form-data",
        "-F",f"file=@{new_name}",
        "-F","model=whisper-1",
        "-F",f"prompt={prompt}",
        "-F","response_format=srt",
        "-F","language=en"
    ]
   
    # Run the cURL command as a subprocess with the console window hidden
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8') 

    # extract the SRT portion from the response
    stdout_lines = result.stdout.splitlines()
    srt_lines = ['1'] + stdout_lines[1:] # add the first line with "1" and start extracting from the second line
    srt_text = "\n".join(srt_lines)
    os.remove("transcribe.mp3")

    return srt_text

# function to save transcription as Srt file
def save_transcription_as_srt(transcription, audio_path):
    
    # Use the local file name without the extension
    video_title = os.path.splitext(os.path.basename(audio_path))[0]

    subtitle_path = f"video-subtitles/{video_title}.srt"

    with open(subtitle_path, "w", encoding='utf-8') as f:
        f.write(transcription)
    
    return subtitle_path


def convert_to_mp3(input_file_path, quality):
    output_audio = f"video-audio/{os.path.basename(os.path.splitext(input_file_path)[0])}.mp3"
    try: 
        subprocess.run(
            [
                "ffmpeg",
                "-y",  # Add the '-y' option to overwrite the output file without confirmation
                "-i",
                input_file_path,
                "-vn",
                "-acodec",
                "libmp3lame",
                "-b:a",
                f"{quality}k",
                output_audio,
            ],
            check=True,
        )
        print(f"Successfully extracted audio to {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        
    return output_audio

'''
def local_whisper(audio_file, model, language, prompt):
    audio_path = audio_file
    model = model
    output_format = "srt"
    temperature = 0.0 #at zero, basically turns off best_of
    best_of = 5

    if language:
        cmd = ['whisper', 
                audio_path, 
                '--model', model, 
                '--output_dir', ".", 
                '--output_format', output_format,
                '--initial_prompt', prompt,
                '--language', language,
                '--temperature', f'{temperature}',
                '--best_of',  f'{best_of}']
    else:
        cmd = ['whisper', 
                audio_path, 
                '--model', model, 
                '--output_dir', ".", 
                '--output_format', output_format,
                '--initial_prompt', prompt,
                '--temperature', f'{temperature}',
                '--best_of', f'{best_of}']

    subprocess.run(cmd)
'''