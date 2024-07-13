import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from input_handling import pdf_to_chapters
from audio_convert import audio_converter

def add_row():
    """Add a new row to the table."""
    row_number = len(entries)
    chapter = Label(chapters, text=f"ch{row_number}")
    chapter.grid(row=len(entries)+1, column=0)

    keyword_entry = Entry(chapters)
    keyword_entry.grid(row=len(entries)+1, column=1)

    output_dir = directory_entry.get()
    input_file_path = os.path.join(output_dir, f"{chapter}.txt")
    output_file_path = os.path.join(output_dir, f"/audio")

    convert_button = Button(chapters, text="Convert", command=audio_converter(textfile_path=input_file_path, speaker_voice=voices.get(), output_dir=output_file_path))
    convert_button.grid(row=len(entries)+1, column=2)

    entries.append((chapter, keyword_entry))

def get_content_list():
    """Retrieve the content list from the table."""
    content_list = []
    for chapter_entry, keyword_entry in entries:
        chapter = chapter_entry.get()
        keyword = keyword_entry.get()
        if chapter and keyword:
            content_list.append((chapter, keyword))
    return content_list

def generate():
    """Collect inputs and call the pdf_to_chapters function."""
    pdf_path = pdf_entry.get()
    output_dir = directory_entry.get()
    start_page = int(from_page_entry.get())
    end_page = int(to_page_entry.get())
    content_list = get_content_list()
    pdf_to_chapters(pdf_path, start_page, end_page, content_list, output_dir)  

def pdf_upload():
    """Open file browser for pdf"""
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File",
                                          filetypes = (("PDF files", "*.pdf"), ("all files", "*.*")))
    pdf_entry.config(state=NORMAL)
    pdf_entry.delete(0, END)
    pdf_entry.insert(0, filename)
    pdf_entry.config(state='readonly')

def browseDirectory():
    """Open file browser for output directory"""
    foldername = filedialog.askdirectory(initialdir = "/", title = "Select a Folder")
    
    directory_entry.config(state=NORMAL)
    directory_entry.delete(0, END)
    directory_entry.insert(0, foldername)
    directory_entry.config(state='readonly')


def get_voice_files(directory):
    """Get the list of voice files from the specified directory."""
    voice_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return voice_files
      
# ---------------------------- UI SETUP ---------------------------
window = Tk()
window.title("Audiobook Generator")
window.config(padx=50, pady=50)


#File Uploader
file_uploader = Frame(window)
file_uploader.grid(row=0, column=0, columnspan=3)

pdf_label = Label(file_uploader, text="Upload PDF File")
pdf_label.grid(row=0, column=0)

pdf_button = Button(file_uploader, text="Upload", command=pdf_upload)
pdf_button.grid(row=0, column=1)

pdf_entry = Entry(file_uploader, width=38, state='readonly')
pdf_entry.grid(row=1, column=0, columnspan=2)


#Output Path
directory_label = Label(file_uploader, text="Choose Output Folder:")
directory_label.grid(row=2, column=0)

directory_button = Button(file_uploader, text="Browse", command=browseDirectory)
directory_button.grid(row=2, column=1)

directory_entry = Entry(file_uploader, width=38, state='readonly')
directory_entry.grid(row=3, column=1, columnspan=2)


#Audio Selector
Label(file_uploader, text="Choose Audio").grid(row=4, column=0)

script_dir = os.path.dirname(os.path.abspath(__file__))
voices_dir = os.path.join(script_dir, 'voices')
voice_files = get_voice_files(voices_dir)

voices = ttk.Combobox(file_uploader, state="readonly", values=voice_files)
voices.grid(row=4, column=1)
voices.current(0)


#begining & ending
from_page = Label(file_uploader, text="From Page:")
from_page.grid(row=5, column=0)

from_page_entry = Entry(file_uploader, width=8)
from_page_entry.grid(row=5, column=1)

to_page = Label( file_uploader, text="To Page:")
to_page.grid(row=6, column=0)

to_page_entry = Entry(file_uploader, width=8)
to_page_entry.grid(row=6, column=1)

generate_button = Button(file_uploader, text="Generate", command=generate)
generate_button.grid(row=7, column=0, columnspan=2)

#Chapters Table
chapters = Frame(window)
chapters.grid(row=0, column=4, columnspan=2)

Label(chapters, text="Chapter").grid(row=0, column=0)
Label(chapters, text="Start Keyword").grid(row=0, column=1)

entries = [] # Store entries in a list
add_row() # Add the first row
add_button = Button(chapters, text="Add Row", command=add_row)
add_button.grid(row=0, column=2)


window.mainloop()


#Later
#TODO: work on the UX of GUI
#DONE: audio converter
#DONE: File upload


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling
#TODO: Generate the YT cover automatically