"""
audio_trancriber.py

This module defines the audio_transcriber_tool which:
- Downloads the audio stream from a given YouTube URL.
- Uses the Whisper model to transcribe the audio.
- Returns the transcribed text.

The tool is registered with CrewAI using the @tool decorator, making it accessible to agents.
"""

# Import the necessary modules.
from crewai_tools import tool
from pytube import YouTube
import whisper

@tool("Audio Transribe tool")
def audio_transcriber_tool(url):
    """
    Extracts audio from a YouTube video and transcribes it using the Whisper model.

    Parameters:
        url (str): The URL of the YouTube video from which audio will be extracted.

    Returns:
        str: The transcribed text from the video audio.

    Process:
        1. Use pytube to get the YouTube video object.
        2. Filter for audio-only streams and download the first available one.
        3. Load the Whisper model (using the "small" model for balance between speed and accuracy).
        4. Transcribe the downloaded audio file.
        5. Return the transcription text.
    """
    # Create a YouTube object using the provided URL.
    yt = YouTube(url)

    # Select the first audio-only stream available.
    video = yt.streams.filter(only_audio=True).first()

    # Download the audio stream; the file is saved locally.
    out_file = video.download()

    # Optional: Gather video details (e.g., title) for potential logging or future use.
    video_details = {
        "name": yt.title,
    }

    # Load the Whisper model (using the 'small' model variant).
    whisper_model = whisper.load_model("small")

    # Transcribe the downloaded audio file.
    result = whisper_model.transcribe(out_file)

    # Return the transcribed text.
    return result["text"]
