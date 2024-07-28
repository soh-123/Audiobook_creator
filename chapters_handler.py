import os
from tkinter import *
from tkinter import ttk  # Make sure to import ttk
from audio_convert import audio_converter

def get_voice_files(directory):
    """Get list of voice files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.mp3') or f.endswith('.wav')]

class ChapterHandler:
    def __init__(self, chapters_frame, canvas, scrollbar, directory_entry, voices, voices_dir):
        self.entries = []
        self.chapters_frame = chapters_frame
        self.canvas = canvas
        self.scrollbar = scrollbar
        self.directory_entry = directory_entry
        self.voices = voices
        self.voices_dir = voices_dir

    def add_row(self):
        """Add a new row to the table"""
        row_number = len(self.entries)
        chapter_label_text = f"ch{row_number}"

        chapter_label = Label(self.chapters_frame, text=chapter_label_text)
        chapter_label.grid(row=row_number + 1, column=0, sticky='ew')

        keyword_entry = Entry(self.chapters_frame)
        keyword_entry.grid(row=row_number + 1, column=1, sticky='ew')

        status_label = Label(self.chapters_frame, text="", fg="green")
        status_label.grid(row=row_number + 1, column=3, sticky='ew')

        convert_button = Button(self.chapters_frame, text="Convert", command=lambda: self.convert_audio(chapter_label_text, status_label))
        convert_button.grid(row=row_number + 1, column=2, sticky='ew')

        self.entries.append((chapter_label, keyword_entry))

        # Enable scrollbar if more than 8 rows
        if len(self.entries) > 8:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.scrollbar.pack(fill=Y, side=LEFT, expand=FALSE)
        else:
            self.scrollbar.pack_forget()

    def convert_audio(self, chapter_label_text, status_label):
        """Convert text to audio."""
        output_dir = self.directory_entry.get()
        input_file_path = os.path.join(output_dir, f"{chapter_label_text}.txt")
        output_file_path = os.path.join(output_dir, "audio", f"{chapter_label_text}.wav")

        audio_dir = os.path.dirname(output_file_path)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir, exist_ok=True)

        voice_pick = os.path.join(self.voices_dir, self.voices.get())
        print(f"Converting {input_file_path} using voice {self.voices.get()}")
        audio_converter(textfile_path=input_file_path, speaker_voice=voice_pick, output_dir=audio_dir)
        
        status_label.config(text=f"Conversion for {chapter_label_text} completed!")

    def get_content_list(self):
        """Retrieve the content list from the table."""
        content_list = []
        for chapter_label, keyword_entry in self.entries:
            chapter = chapter_label.cget("text")
            keyword = keyword_entry.get().strip()

            content_list.append((chapter, keyword))
           
        return content_list
