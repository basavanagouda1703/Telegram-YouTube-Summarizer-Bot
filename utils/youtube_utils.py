import re
import requests


def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    if match:
        return match.group(1)

    match = re.search(r"youtu\.be/([^?&]+)", url)
    if match:
        return match.group(1)

    return None


def fetch_video_title(video_id):
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url)
        data = response.json()
        return data["title"]
    except:
        return "YouTube Video"