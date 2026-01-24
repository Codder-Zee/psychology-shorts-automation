from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

with open("token.pickle", "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

title = open("output/title.txt").read()
description = open("output/script.txt").read()

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("output/final.mp4")
)

response = request.execute()
print("Uploaded:", response["id"])
