
"""
Voice handler — transcribes audio files using OpenAI's transcription model.
"""

import os
from typing import Optional
from learning_agent.exceptions import MissingApiKeyError


TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
SUPPORTED_AUDIO_FORMATS = {".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"}


def transcribe_audio(audio_bytes: bytes, filename: str) -> Optional[str]:
    """
    Transcribe audio content to text using OpenAI's transcription API.

    Args:
        audio_bytes: Raw bytes of the audio file.
        filename: Original filename (used to determine MIME type).

    Returns:
        Transcribed text string, or None if transcription fails.

    Raises:
        ValueError: If the audio format is not supported.
        MissingApiKeyError: If OPENAI_API_KEY is not set.
    """
    import io
    from openai import OpenAI

    ext = _get_extension(filename)
    if ext not in SUPPORTED_AUDIO_FORMATS:
        raise ValueError(
            f"Unsupported audio format: '{filename}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_AUDIO_FORMATS))}"
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MissingApiKeyError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename

    response = client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file,
    )

    return response.text.strip()


def _get_extension(filename: str) -> str:
    """Extract the lowercase file extension including the dot."""
    dot_index = filename.rfind(".")
    if dot_index == -1:
        return ""
    return filename[dot_index:].lower()
