import torch
from TTS.api import TTS
from IPython.display import Audio
import os
from pydub import AudioSegment

#DONE: read each chapter by dividing them into chunks and create the audio pieces
#DONE: combine all audio pieces into one
#DONE: Extract each chapter alone

device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
print(TTS().list_models()) # List available 🐸TTS models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # Initialize TTS

def split_text(text, chunk_size=250):
    """dividing text into chunks of 250 character for a better audio quality"""
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


def chunk_converter(textfile_path, speaker_voice, output_dir):
    """
    Convert a chapter file into audio chunks using a specified voice.

    - Requires Nvidia GPU to run
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the input text file
    with open(textfile_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split the text into chunks
    text_chunks = split_text(text)

    for i, chunk in enumerate(text_chunks):
        output_file_path = os.path.join(output_dir, f"ch{i}.wav")
        tts.tts_to_file(text=chunk, speaker_wav=speaker_voice, language="en", file_path=output_file_path)
    print("audio converter finished!")


def combine_chunks(audio_dir, prefix):
    """
    Combine audio chunks into a single audio file.
    """
    # List all files in the directory with the specified prefix and .wav extension
    files = [f for f in os.listdir(audio_dir) if f.startswith(prefix) and f.endswith('.wav')]

     # Sort files based on the numeric part of the filename
    files.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))
    
    # Create an empty AudioSegment to append the chunks
    combined = AudioSegment.empty()
    
    # Loop through each file and append it to the combined audio segment
    for file in files:
        audio_path = os.path.join(audio_dir, file)
        current_audio = AudioSegment.from_wav(audio_path)
        combined += current_audio

    output_path = os.path.join(audio_dir, f'combined_audio-{prefix}.wav')
    combined.export(output_path, format='wav')

    print(f"Combined audio saved to {output_path}")
