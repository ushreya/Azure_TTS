# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:10:49 2024

@author: shreya
"""
import azure.cognitiveservices.speech as speechsdk
import os

# Set up speech configuration with subscription key and region
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

# Define the output directory for synthesized audio files
output_dir = "D:/shreya/TTS_LLM/output_audio/"
os.makedirs(output_dir, exist_ok=True)

# Function to create SSML with specific voice and style
def create_ssml(text, voice="en-US-JennyNeural", style="friendly"):
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='{voice}' style='{style}'>{text}</voice>
    </speak>
    """
    return ssml

# Function to perform batch synthesis with SSML
def batch_synthesis(texts):
    for idx, text in enumerate(texts):
        # Create SSML for the text
        ssml = create_ssml(text)

        # Create a speech synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

        # Synthesize the text using SSML
        result = synthesizer.speak_ssml_async(ssml).get()

        # Save the audio data to a file
        filename = f"sample_{idx}.mp3"
        with open(os.path.join(output_dir, filename), "wb") as file:
            file.write(result.audio_data)
        print(f"Audio saved: {filename}")

# Example usage
if __name__ == "__main__":
    texts = [
        "Hello, how are you?",
        "This is a batch synthesis example.",
        "You can synthesize multiple texts at once."
    ]
    batch_synthesis(texts)