import asyncio
import edge_tts

async def _generate_audio_async(text: str, output_path: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-PrabhatNeural"
    )
    await communicate.save(output_path)


def generate_audio(text: str, output_path: str):
    if not text.strip():
        print("Empty text")
        return
    
    asyncio.run(_generate_audio_async(text, output_path))
    print("Audio saved to:", output_path)


if __name__ == "__main__":
    user_input = input("Enter text to speak: ")
    generate_audio(user_input, "response.mp3")