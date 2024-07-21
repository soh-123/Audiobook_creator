import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from input_handling import pdf_to_chapters
from audio_convert import audio_converter
from chapters_handler import ChapterHandler


def generate():
    """Collect inputs and call the pdf_to_chapters function."""
    pdf_path = pdf_entry.get()
    start_page = int(from_page_entry.get())
    end_page = int(to_page_entry.get())
    content_list = chapter_handler.get_content_list()
    output_dir = directory_entry.get()
    print(f"here's the content list{content_list}")
    pdf_to_chapters(pdf_path=pdf_path, start=start_page, end=end_page, content_list=content_list, output_dir=output_dir)  


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


def get_voice_files(directory):
    """Get the list of voice files from the specified directory."""
    voice_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return voice_files
      
# ---------------------------- UI SETUP ---------------------------
window = Tk()
window.title("Audiobook Generator")
window.config(padx=50, pady=50)

# Make the window resizable
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(4, weight=1)

#File Uploader
file_uploader = Frame(window)
file_uploader.grid(row=0, column=0, columnspan=3, sticky="nsew")

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
chapters_frame = Frame(window)
chapters_frame.grid(row=0, column=4, sticky='nsew')

chapters_frame.rowconfigure(0, weight=1)
chapters_frame.columnconfigure(0, weight=1)

canvas = Canvas(chapters_frame)
scrollbar = Scrollbar(chapters_frame, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
chapters = Frame(canvas)
chapters.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=chapters, anchor="nw")
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)
scrollbar.pack_forget()

Label(chapters, text="Chapter").grid(row=0, column=0)
Label(chapters, text="Start Keyword").grid(row=0, column=1)

# Initialize the ChapterHandler
chapter_handler = ChapterHandler(chapters, canvas, scrollbar, directory_entry, voices)
chapter_handler.add_row()  # Add the first row

add_button = Button(chapters, text="Add Row", command=chapter_handler.add_row)
add_button.grid(row=0, column=2)

window.mainloop()


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling
#TODO: Generate the YT cover automatically