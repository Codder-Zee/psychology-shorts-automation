import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

REQUIRED = ["YT_REFRESH_TOKEN", "YT_CLIENT_ID", "YT_CLIENT_SECRET"]
for k in REQUIRED:
    if not os.getenv(k):
        raise Exception(f"Missing env variable: {k}")

creds = Credentials(
    token=None,
    refresh_token=os.environ["YT_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["YT_CLIENT_ID"],
    client_secret=os.environ["YT_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

youtube = build("youtube", "v3", credentials=creds)

if not os.path.exists("final_video.mp4"):
    raise Exception("final_video.mp4 not found")

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": os.getenv("VIDEO_TITLE", "Psychology Secret"),
            "description": os.getenv("VIDEO_DESC", ""),
            "categoryId": "27"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("final_video.mp4", resumable=True)
)

request.execute()
print("✅ YouTube upload successful")
