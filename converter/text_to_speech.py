import asyncio
import edge_tts
from pathlib import Path

class TextToSpeech:
    def __init__(self, voice: str):
        self.voice = voice
    
    async def generate_speech_with_timing(self, text: str, output_path: str) -> float:
        communicate = edge_tts.Communicate(text, self.voice)
        
        # Ensure the output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save the audio file
        await communicate.save(output_path)
        
        # Estimate duration based on word count (rough estimate)
        # Assuming average speaking rate of 3 words per second
        duration = len(text.split()) / 3
        return duration
        
    def generate_speech(self, text: str, output_path: str) -> float:
        """
        Generates speech from text and saves it to the specified path
        Returns the duration of the generated audio in seconds
        """
        return asyncio.run(self.generate_speech_with_timing(text, output_path)) 