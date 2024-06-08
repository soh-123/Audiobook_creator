import torch
from TTS.api import TTS
from IPython.display import Audio
import os
from pydub import AudioSegment

device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
print(TTS().list_models()) # List available 🐸TTS models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # Initialize TTS

def split_text(text, chunk_size=250):
    """dividing each text file into chunks of 250 character for a better audio quality"""
    chunks = []
    current_chunk = []
    current_length = 0

    for word in text.split():
        word_length = len(word) + 1  # +1 to account for the space after each word
        if current_length + word_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def chunk_converter(textfile_path, speaker_voice):
    with open(textfile_path, 'r', encoding='utf-8') as f:
        text = f.read()

    text_chunks = split_text(text)

    for i, chunk in enumerate(text_chunks):
        tts.tts_to_file(text=chunk, speaker_wav=speaker_voice, language="en", file_path=f"/kaggle/working/ch3-{i}.wav")
    print("audio converter finished!")


def combine_chunks(audio_dir):
    files = [f for f in os.listdir(audio_dir) if f.startswith('ch3-') and f.endswith('.wav')]
    files.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))
    combined = AudioSegment.empty()
    
    # Loop through each file and append it to the combined audio segment
    for file in files:
        audio_path = os.path.join(audio_dir, file)
        current_audio = AudioSegment.from_wav(audio_path)
        combined += current_audio

    output_path = os.path.join(audio_dir, 'combined_audio.wav')
    combined.export(output_path, format='wav')

    print(f"Combined audio saved to {output_path}")


audio_dir = '/kaggle/working/'
textfile_path = '/content/chapter16.txt'
speaker_voice = "/kaggle/input/djano-voice/Djano.mp3"
chunk_converter(textfile_path, speaker_voice)
combine_chunks(audio_dir)