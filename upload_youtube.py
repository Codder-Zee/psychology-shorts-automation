from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

youtube = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Psychology ka ye sign ignore mat karo",
            "description": "Hindi psychology facts #shorts",
            "categoryId": "27"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("short.mp4")
)

request.execute()
