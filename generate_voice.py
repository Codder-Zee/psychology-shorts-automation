import edge_tts, asyncio
import os

async def main():
    if not os.path.exists("script.txt"):
        print("Error: script.txt nahi mili!")
        return
        
    text = open("script.txt", encoding="utf-8").read().strip()
    if not text:
        print("Error: script.txt khali hai!")
        return

    print("Voice generate ho rahi hai...")
    tts = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural")
    await tts.save("voice.mp3")
    print("voice.mp3 save ho gayi!")

if __name__ == "__main__":
    asyncio.run(main())
  
