from googleapiclient.discovery import build
import re
from datetime import timedelta

api_key = "AIzaSyA7s5GfVuWrbTCWaqOAzTKoGOrpQ96yacY"

youtube = build("youtube", "v3",developerKey=api_key)

request = youtube.channels().list(
    part="statistics",
    forUsername="sentdex"
)

response = request.execute()
channel_id = response["items"][0]["id"]


hour_pattern = re.compile(r"(\d+)H")
minute_pattern = re.compile(r"(\d+)M")
second_pattern = re.compile(r"(\d+)S")

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for items in pl_response["items"]:
        vid_ids.append(items["contentDetails"]["videoId"])

    vid_request = youtube.videos().list(
        part="contentDetails",
        id=",".join(vid_ids)
    )
    vid_response = vid_request.execute()

    
    for item in vid_response["items"]:
        duration = item["contentDetails"]["duration"]
        
        hours = hour_pattern.search(duration)
        minutes = minute_pattern.search(duration)
        seconds = second_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()

        print(video_seconds)
        print()
    nextPageToken = pl_response.get("nextPageToken")
    if not nextPageToken:
        break




