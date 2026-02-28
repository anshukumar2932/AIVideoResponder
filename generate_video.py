import os
import random
import subprocess
import asyncio
import edge_tts

DATASET_PATH = "dataset/viseme_dataset_aligned"

TEMP_VIDEO = "temp_concat.mp4"
FINAL_VIDEO = "final.mp4"
AUDIO_FILE = "response.mp3"

VISEME_MAP = {
    "a": "viseme_open",
    "e": "viseme_wide",
    "i": "viseme_wide",
    "o": "viseme_round",
    "u": "viseme_round",
    "b": "viseme_full_closed",
    "p": "viseme_full_closed",
    "m": "viseme_full_closed",
    "f": "viseme_partial_closed",
    "v": "viseme_partial_closed",
    "s": "viseme_sibilant",
    "z": "viseme_sibilant",
    "t": "viseme_tongue",
    "d": "viseme_tongue",
    "n": "viseme_tongue",
    "l": "viseme_tongue",
    "r": "viseme_neutral",
    "k": "viseme_neutral",
    "g": "viseme_neutral",
    "h": "viseme_neutral",
    "j": "viseme_neutral",
    "q": "viseme_neutral",
    "w": "viseme_round",
    "x": "viseme_sibilant",
    "y": "viseme_wide",
}


def text_to_visemes(text):
    words = text.lower().split()
    return [VISEME_MAP.get(word[0], "viseme_neutral") for word in words]


def select_clip(viseme):
    folder_path = os.path.join(DATASET_PATH, viseme)
    files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    return os.path.join(folder_path, random.choice(files))


def create_concat_file(clip_paths, filename="list.txt"):
    with open(filename, "w") as f:
        for path in clip_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
    return filename


def concatenate_clips(list_file, output_video):
    command = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_video
    ]
    subprocess.run(command, check=True)


def attach_audio(video_path, audio_path, final_output):
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        final_output
    ]
    subprocess.run(command, check=True)


def generate_video(text, audio_path, output_path):
    viseme_sequence = text_to_visemes(text)
    clip_paths = [select_clip(v) for v in viseme_sequence]

    list_file = create_concat_file(clip_paths)
    concatenate_clips(list_file, TEMP_VIDEO)
    attach_audio(TEMP_VIDEO, audio_path, output_path)

    os.remove(list_file)
    os.remove(TEMP_VIDEO)

    print("✅ Video generated:", output_path)


async def generate_audio(text: str, output_path: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-PrabhatNeural"
    )
    await communicate.save(output_path)


def main():
    text = "Your order has been cancelled, thank you for shopping with us."

    print("🎤 Generating audio...")
    asyncio.run(generate_audio(text, AUDIO_FILE))

    print("🎬 Generating video...")
    generate_video(text, AUDIO_FILE, FINAL_VIDEO)


if __name__ == "__main__":
    main()