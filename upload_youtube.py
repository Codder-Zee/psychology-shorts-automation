import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_ID = os.environ["YT_CLIENT_ID"]
CLIENT_SECRET = os.environ["YT_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["YT_REFRESH_TOKEN"]

def get_youtube_service():
    credentials = google.oauth2.credentials.Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    return build("youtube", "v3", credentials=credentials)

def upload_video():
    print("🚀 Starting YouTube upload...")

    youtube = get_youtube_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Psychology Fact You Didn't Know",
                "description": "Generated automatically",
                "tags": ["psychology", "facts", "shorts"],
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload("final.mp4", resumable=True)
    )

    response = request.execute()
    print("✅ Uploaded successfully!")
    print("📺 Video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
