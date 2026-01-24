import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

try:
    CLIENT_ID = os.getenv("YT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        raise Exception("YouTube OAuth secrets missing")

    creds = google.oauth2.credentials.Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    youtube = build("youtube", "v3", credentials=creds)

    video_file = "output/final.mp4"
    title = open("output/title.txt", encoding="utf-8").read().strip()
    description = open("output/script.txt", encoding="utf-8").read()

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=media
    )

    response = request.execute()
    print("✅ VIDEO UPLOADED:", response["id"])

except Exception as e:
    print("❌ YOUTUBE UPLOAD FAILED")
    print("Reason:", e)
    raise
