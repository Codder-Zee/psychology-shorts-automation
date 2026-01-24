import edge_tts, asyncio, os

async def main():
    text = open("output/script.txt", encoding="utf-8").read()
    os.makedirs("output", exist_ok=True)

    tts = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural")
    await tts.save("output/voice.mp3")

asyncio.run(main())
