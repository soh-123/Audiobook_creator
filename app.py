import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F

from IPython.display import Audio

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices
from tortoise.utils.text import split_and_recombine_text
from time import time
import os
import shutil

# Initialize the TextToSpeech model
tts = TextToSpeech()

CUSTOM_VOICE_NAME = "train_lescault"
custom_voice_folder = f"{CUSTOM_VOICE_NAME}"

# Define the input audio directory
input_audio_directory = f"tortoise/voices/train_lescault"

# Copy audio files from the input directory to the custom voice folder with new names
for i, file_name in enumerate(os.listdir(input_audio_directory)):
    input_file_path = os.path.join(input_audio_directory, file_name)
    if os.path.isfile(input_file_path) and input_file_path.endswith('.wav'):
        output_file_path = os.path.join(custom_voice_folder, f'lescault_new{i}.wav')
        shutil.copy(input_file_path, output_file_path)

print("Files copied successfully.")

# Define output and text file paths
outpath = "/"
textfile_path = "/chapter9.txt"

# Process text
with open(textfile_path, 'r', encoding='utf-8') as f:
    text = ' '.join([l.strip() for l in f.readlines()])  # Strip leading/trailing spaces
    texts = split_and_recombine_text(text)

seed = int(time())

voice_outpath = os.path.join(outpath, CUSTOM_VOICE_NAME)
os.makedirs(voice_outpath, exist_ok=True)

voice_samples, conditioning_latents = load_voice(CUSTOM_VOICE_NAME)

all_parts = []
for j, text in enumerate(texts):
    torch.cuda.empty_cache()  # Clear cache before generating each part to avoid memory issues
    
    with torch.cuda.amp.autocast():  # Use automatic mixed precision
        gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents,
                                  preset="high_quality", k=1, use_deterministic_seed=seed)
    gen = gen.squeeze(0).cpu()
    torchaudio.save(os.path.join(voice_outpath, f'{j}.wav'), gen, 24000)
    all_parts.append(gen)

torch.cuda.empty_cache()  # Clear cache before concatenating to avoid memory issues

full_audio = torch.cat(all_parts, dim=-1)
combined_audio_path = os.path.join(voice_outpath, 'combined.wav')
torchaudio.save(combined_audio_path, full_audio, 24000)

# Display the audio
Audio(combined_audio_path)
