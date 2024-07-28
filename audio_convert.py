import torch
from TTS.api import TTS
import os
from pydub import AudioSegment


device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
print(TTS().list_models()) # List available 🐸TTS models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # Initialize TTS

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert an MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def audio_converter(textfile_path, speaker_voice, output_dir):
    """
    Convert a chapter file into audio using a specified voice.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if speaker_voice is in mp3 format and convert to wav if needed
    speaker_voice_wav = speaker_voice
    if speaker_voice.endswith(".mp3"):
        speaker_voice_wav = os.path.splitext(speaker_voice)[0] + ".wav"
        convert_mp3_to_wav(speaker_voice, speaker_voice_wav)

    # Read the input text file  
    with open(textfile_path, 'r') as file:
        text = file.read()

    output_file_path = os.path.join(output_dir, f"{os.path.basename(textfile_path).split('.')[0]}.wav")

    tts.tts_to_file(text=text, 
                    speaker_wav=speaker_voice_wav, 
                    language="en", 
                    file_path=output_file_path, 
                    split_sentences=True)
    
    print("audio converter finished!")


if __name__ == "__main__":
    textfile_path = "/Users/sohierelsafty/Desktop/how to own your own mind/ch0.txt" #converting chapter per chapter
    speaker_voice = "Audiobook_creator/voices/Djano.mp3" #speaker file to clone
    audio_output_dir = "/Users/sohierelsafty/Desktop/how to own your own mind/Audio" #path to the audio output
    audio_converter(textfile_path, speaker_voice, audio_output_dir)
