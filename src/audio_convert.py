import torch
from TTS.api import TTS
import os
from pydub import AudioSegment
import tempfile


device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
print(TTS().list_models()) # List available 🐸TTS models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # Initialize TTS

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def audio_converter(textfile, textbox_text, speaker_voice, history):
    """
    Convert text or text file to audio with a given voice.
    """

     # Decide on the text input
    if textfile is not None:
        with open(textfile.name, 'r', encoding='utf-8') as file:
            text = file.read()
        label = os.path.basename(textfile.name)
    elif textbox_text and textbox_text.strip():
        text = textbox_text.strip()
        label = textbox_text[:30] + ("..." if len(textbox_text) > 30 else "")
    else:
        return history, "Please upload a text file or enter text."
    
    if speaker_voice is None:
        return history, "Please upload a voice file."
    
     # Save voice file to temp location if necessary
    with tempfile.TemporaryDirectory() as tempdir:
        speaker_voice_path = speaker_voice.name
        if speaker_voice_path.endswith(".mp3"):
            speaker_voice_wav = os.path.join(tempdir, "voice.wav")
            convert_mp3_to_wav(speaker_voice_path, speaker_voice_wav)
        else:
            speaker_voice_wav = speaker_voice_path

     # Output audio file
    output_audio = os.path.join(tempdir, f"{os.path.splitext(label)[0]}.wav")
    tts.tts_to_file(text=text, 
                    speaker_wav=speaker_voice_wav, 
                    language="en", 
                    file_path=output_audio, 
                    split_sentences=True)
    
    # Make file available after tempdir closes
    output_copy = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(output_audio, "rb") as src, open(output_copy.name, "wb") as dst:
        dst.write(src.read())

    history.append((label, output_copy.name))
    return history, None
