import torch
from TTS.api import TTS
import os

device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
print(TTS().list_models()) # List available 🐸TTS models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # Initialize TTS


def audio_converter(textfile_path, speaker_voice, output_dir):
    """
    Convert a chapter file into audio using a specified voice.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the input text file  
    with open(textfile_path, 'r') as file:
        text = file.read()

    output_file_path = os.path.join(output_dir, f"file.wav")

    tts.tts_to_file(text=text, 
                    speaker_wav=speaker_voice, 
                    language="en", 
                    file_path=output_file_path, 
                    split_sentences=True)
    
    print("audio converter finished!")


if __name__ == "__main__":
    textfile_path = "/Users/sohierelsafty/Downloads/how to own your own mind/ch1-1.txt" #converting chapter per chapter
    speaker_voice = "Brian.mp3" #speaker file to clone
    audio_output_dir = "/Users/sohierelsafty/Downloads/how to own your own mind/Audio" #path to the audio output
    audio_converter(textfile_path, speaker_voice, audio_output_dir)
