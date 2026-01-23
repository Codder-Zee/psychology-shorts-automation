import sys
import os
import edge_tts
import asyncio

VOICE = "hi-IN-MadhurNeural"
SCRIPT_PATH = "../assets/script.txt"
VOICE_PATH = "../assets/voice.mp3"

class VoiceError(Exception):
    pass

async def generate_voice():
    if not os.path.exists(SCRIPT_PATH):
        raise VoiceError("script.txt missing")

    with open(SCRIPT_PATH, encoding="utf-8") as f:
        text = " ".join(f.readlines())

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(VOICE_PATH)

    print("✅ Voice generated")

if __name__ == "__main__":
    try:
        asyncio.run(generate_voice())
    except Exception as e:
        print("❌ VOICE ERROR:", e)
        sys.exit(1)
