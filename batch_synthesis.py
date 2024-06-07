# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:17:17 2024

@author: shreya
"""

import azure.cognitiveservices.speech as speechsdk
import glob as glob
import os
import random

### Set the Azure connection
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

# Function to create SSML with specific voice and style
def create_ssml(text, voice="en-US-JennyNeural", style="neutral"):
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='{voice}' style='{style}'>{text}</voice>
    </speak>
    """
    return ssml
       
def batch_synthesis(texts, voices, styles):
    selected_voices = {
        "M": random.choice(voice_dict["M"]),
        "F": random.choice(voice_dict["F"])
    }
   
    for idx, (text, gender, style) in enumerate(zip(texts, voices, styles)):
        voice = selected_voices[gender]
        
        # Create SSML for the text
        ssml = create_ssml(text, voice, style)
    
        # Synthesize the text using SSML
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_ssml_async(ssml).get()
    
        # Save the audio
        filename = f"Sample_{idx}.wav"
        with open(os.path.join(output_dir, filename), "wb") as file:
            file.write(result.audio_data)
        
def read_input_file(file_path):
    texts = []
    voices = []
    styles = []
    with open(file_path,  'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('[')
            
            if len(parts)==2:
                voices.append(parts[0].split(":")[0])
                styles.append(parts[-1].replace("]", ""))
                texts.append(parts[0].split(":")[1].strip())
            else: 
                new_part1=''.join(parts[:len(parts)-1])
                new_part1= new_part1.replace(" Ms./Mr. Customer Name]", "")
                voices.append(new_part1.split(":")[0])
                styles.append(parts[-1].replace("]", ""))
                texts.append(new_part1.split(":")[1].strip())
                
    return texts, voices, styles

#%%
if __name__ == "__main__":
    all_file=glob.glob('path_to_txts/*.txt')

    # Specify voices for each text
    voice_dict = {
    "M": [
        "en-US-GuyNeural",
        "en-US-DavisNeural",
        "en-US-JasonNeural",
        "en-US-TonyNeural"
        ],
    "F": [
        "en-US-JaneNeural",
        "en-US-JennyNeural",
        "en-US-AriaNeural",
        "en-US-SaraNeural",
        "en-US-NancyNeural"
        ]
    }
    # Specify emotion style for each text
    style_dict = {
        "Neutral":"Neutral", 
        "Happy":"Cheerful",  
        "Sad":"Sad",     
        "Angry":"Angry"}

    for fil in all_file:
        
        fname=fil.split("\\")[-1].replace(".txt", "")
        
        output_dir = "path_to_output_dir/{}/".format(fname)
        os.makedirs(output_dir, exist_ok=True)
            
        texts, voices, style =  read_input_file(fil)
            
        styles =  [style_dict[s] for s in style]
                
        batch_synthesis(texts, voices, styles)
  
 
############################ CHECK FOR CORRUPTED WAV FILES 
import librosa
from collections import Counter

def check_wav_file(file_path):
    try:
        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)
        
        # Check the duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Print the duration
        print(f"Duration: {duration} seconds")
        
        # Check if duration is greater than zero
        if duration > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return False

if __name__ == "__main__":
    ggg=glob.glob('path_to_wav/*/*.wav')
    ls=[]
    for i in ggg:
        i
        ff= i.split("\\")[-2]
        is_valid = check_wav_file(i)   
        if not is_valid:
            ls.append(ff)
            
    currupted_folders=list(Counter(ls).keys())
    print("Corrupted files:", len(currupted_folders))
