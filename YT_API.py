from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re
from datetime import timedelta


load_dotenv()
api_key = os.getenv("api_key")

youtube = build("youtube", "v3", developerKey=api_key)

user_name = input("Enter username of channel: ") 
request_channel = youtube.channels().list(
    part="statistics",
    forUsername=user_name
)

response_channel = request_channel.execute()
channel_id = response_channel["items"][0]["id"] 


request_playlist = youtube.playlists().list(
    part="snippet, contentDetails",
    channelId=channel_id,
    maxResults=50
)

response_playlist = request_playlist.execute()

title = input("Enter the title of playlist: ")
for playlist in response_playlist['items']:
        if playlist['snippet']['title'] == title:   
            print(f"Title: {playlist['snippet']['title']}")


playlist_id = playlist["id"]


hour_pattern = re.compile(r"(\d+)H")
minute_pattern = re.compile(r"(\d+)M")
second_pattern = re.compile(r"(\d+)S")


total_seconds = 0

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
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

        total_seconds += video_seconds
    nextPageToken = pl_response.get("nextPageToken")
    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f"Duration: {hours}H:{minutes}M:{seconds}S")
