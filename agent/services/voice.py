import speech_recognition as sr
import os
from services.vault import vault
from openai import OpenAI

class VoiceService:
    """
    Handles audio transcription using OpenAI Whisper (if key available) 
    or Google Speech Recognition (fallback).
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes the given audio file to text.
        """
        # Check for OpenAI Key first for high-quality Whisper transcription
        openai_key = vault.get_secret("OPENAI_API_KEY")
        if openai_key:
            try:
                client = OpenAI(api_key=openai_key)
                with open(audio_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                    )
                return transcript.text
            except Exception as e:
                print(f"[Voice] OpenAI Whisper failed, falling back to Google: {e}")

        # Fallback to Google Speech Recognition (Free, no key needed for basic use)
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return "Audio could not be understood."
        except sr.RequestError as e:
            return f"Could not request results from speech service; {e}"
        except Exception as e:
            return f"Transcription error: {str(e)}"

voice_service = VoiceService()
