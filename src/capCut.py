from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip
import tempfile, os

def combine_audio(audio_files):
    combined = AudioSegment.empty() # Initialize an empty audio segment
    for file in audio_files:
        if file is None or not hasattr(file, "name"):
            raise ValueError("Invalid audio file.")
        audio = AudioSegment.from_file(file.name)
        combined += audio

    # Save combined audio to temp WAV
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    combined.export(temp_out.name, format='wav')
    temp_out.close()
    return temp_out.name 

def full_video(combined_audio_path, cover_image_path):
    audio_clip = AudioFileClip(combined_audio_path)
    img_clip = ImageClip(cover_image_path).set_duration(audio_clip.duration)
    video = img_clip.set_audio(audio_clip)
    temp_video_out = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video.write_videofile(temp_video_out.name, fps=1, codec='libx264', audio_codec='aac', verbose=False, logger=None)
    return temp_video_out.name

def gradio_callback(audio_files, cover_image):
    # 1. Combine the audio files
    combined_audio_path = combine_audio(audio_files)
    # 2. Make video with cover
    video_path = full_video(combined_audio_path, cover_image)
    # 3. Optionally: clean up combined audio file if you wish
    os.unlink(combined_audio_path)
    return video_path
