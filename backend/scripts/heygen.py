import os
import time
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("HEYGEN_API_KEY")

def generate_video(script_text,
                   avatar_id="Daisy-inskirt-20220818",
                   avatar_style="normal",
                   voice_id="2d5b0e6cf36f460aa7fc47e3eee4ba54",
                   background_color="#008000",
                   width=1280,
                   height=720):
    """
    Sends a request to HeyGen's V2 video generate endpoint using the provided script text.
    
    :param script_text: The text/script that will be used for the matching voiceover.
    :param avatar_id:   ID of the avatar to use.
    :param avatar_style: Style of the avatar.
    :param voice_id:    ID of the voice to use.
    :param background_color: Background color for the video.
    :param width:       Video width.
    :param height:      Video height.
    :return: A tuple containing the video_id and the headers used for further requests.
    """
    url = "https://api.heygen.com/v2/video/generate"
    
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": avatar_style
                },
                "voice": {
                    "type": "text",
                    "input_text": script_text,
                    "voice_id": voice_id
                },
                "background": {
                    "type": "color",
                    "value": background_color
                }
            }
        ],
        "dimension": {
            "width": width,
            "height": height
        }
    }
    
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    
    response_data = response.json()
    video_id = response_data.get("data", {}).get("video_id")
    if not video_id:
        raise Exception("Failed to retrieve video_id from the API response.")
    
    return video_id, headers

def poll_video_status(video_id, headers, v_uuid):
    """
    Polls the HeyGen API for the status of the generated video until it's completed.
    Once completed, the video is downloaded and saved locally.
    
    :param video_id: The video ID returned from the generate endpoint.
    :param headers:  Headers used for the API requests.
    """
    video_status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    
    acceptable_statuses = ["processing", "pending", "waiting"]
    
    while True:
        response = requests.get(video_status_url, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {})
        status = data.get("status")
        
        if status == "completed":
            video_url = data.get("video_url")
            thumbnail_url = data.get("thumbnail_url")
            print(f"Video generation completed!\nVideo URL: {video_url}\nThumbnail URL: {thumbnail_url}")
            
            # Download and save the video to a file
            video_filename = f"media/videos/{v_uuid}.mp4"
            video_content = requests.get(video_url).content
            with open(video_filename, "wb") as video_file:
                video_file.write(video_content)
            print(f"Video saved as '{video_filename}'")
            break
        
        elif status in acceptable_statuses:
            print(f"Video is still {status}. Checking status in 5 seconds...")
            time.sleep(5)
        
        elif status == "failed":
            error = data.get("error", "Unknown error")
            print(f"Video generation failed: {error}")
            break
        
        else:
            print(f"Unexpected status received: {status}. Retrying in 5 seconds...")
            time.sleep(5)

def get_video(v_uuid,
              script_text,
              avatar_id="Daisy-inskirt-20220818",
              voice_id="2d5b0e6cf36f460aa7fc47e3eee4ba54"):
    print(avatar_id)
    video_id, headers = generate_video(script_text,
                   avatar_id=avatar_id,
                   voice_id=voice_id,
                   background_color="#008000",
                   width=1080/2,
                   height=1920/2)
    print(f"Video generation started. Video ID: {video_id}")
    poll_video_status(video_id, headers, v_uuid)
    

