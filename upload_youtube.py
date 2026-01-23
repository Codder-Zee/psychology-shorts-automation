from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

with open("token.pickle", "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Psychology Truth That Changes You",
            "description": "Hindi psychology short",
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("final_short.mp4")
)

response = request.execute()
print("✅ Uploaded:", response["id"])
