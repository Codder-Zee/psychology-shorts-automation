import asyncio
import edge_tts

async def generate_voice(text, output="voice.mp3"):
    communicate = edge_tts.Communicate(
        text=text,
        voice="hi-IN-MadhurNeural"
    )
    await communicate.save(output)

if __name__ == "__main__":
    import sys
    asyncio.run(generate_voice(sys.argv[1]))
