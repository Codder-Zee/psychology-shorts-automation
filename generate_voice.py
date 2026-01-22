import edge_tts, asyncio

async def main():
    text = open("script.txt", encoding="utf-8").read()
    tts = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural")
    await tts.save("voice.mp3")

asyncio.run(main())
