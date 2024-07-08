from tkinter import *
from input_handling import pdf_to_chapters

def add_row():
    """Add a new row to the table."""
    chapter_entry = Entry(frame)
    keyword_entry = Entry(frame)
    chapter_entry.grid(row=len(entries)+1, column=0)
    keyword_entry.grid(row=len(entries)+1, column=1)
    entries.append((chapter_entry, keyword_entry))

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

# ---------------------------- UI SETUP ---------------------------
window = Tk()
window.title("Audiobook Generator")
window.config(padx=50, pady=50)

#Table
frame = Frame(window)
frame.grid(row=0, column=4, columnspan=2)

Label(frame, text="Chapter").grid(row=0, column=0)
Label(frame, text="Start Keyword").grid(row=0, column=1)

entries = [] # Store entries in a list
add_row() # Add the first row
add_button = Button(frame, text="Add Row", command=add_row)
add_button.grid(row=0, column=2)

#labels
pdf_label = Label(text="Paste PDF file path:")
pdf_label.grid(row=0, column=0)

directory_label = Label(text="Paste Directory output path:")
directory_label.grid(row=1, column=0)

from_page = Label(text="From Page:")
from_page.grid(row=2, column=0)

to_page = Label(text="To Page:")
to_page.grid(row=2, column=2)


#entries
pdf_entry = Entry(width=38)
pdf_entry.grid(row=0, column=1, columnspan=2)
pdf_entry.focus()

directory_entry = Entry(width=38)
directory_entry.grid(row=1, column=1, columnspan=2)

from_page_entry = Entry(width=8)
from_page_entry.grid(row=2, column=1)

to_page_entry = Entry(width=8)
to_page_entry.grid(row=2, column=3)


#buttons
generate_button = Button(text="Generate", command=generate)
generate_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

# from audio_convert import extract_text_from_pdf, chapters_generator
# from audio_convert import chunk_converter, combine_chunks


# if __name__ == "__main__":
#     pdf_path = "./book.pdf"  # Path to the input PDF book
#     txt_path = "./book.txt"  # Path to the output text book
#     output_dir = "./book-folder" #Path to the book folder 
#     from_page = 15 #start page
#     to_page = 782 #end page

#     #Enter chapters manually to be divided
#     content_list = [
#     ('Introduction', 'PREFACE'),
#     ('Ch1', 'Chapter 1'),
#     ('Ch2', 'Chapter 2'),
#     ('Ch3', 'Chapter 3'),
#     ('Ch4', 'Chapter 4'),
#     ('Ch5', 'Chapter 5'),
#     ]

#     extract_text_from_pdf(pdf_path, txt_path, from_page, to_page)
#     chapters_generator(txt_path, content_list, output_dir)


#     textfile_path = "./book-folder/ch1" #converting chapter per chapter
#     speaker_voice = "Djano.mp3" #speaker name
#     audio_output_dir = "/audio-folder" #path to the audio output
#     prefix = "ch1"  # Example prefix for chapter 1
    
#     chunk_converter(textfile_path, speaker_voice, audio_output_dir, prefix)
#     combine_chunks(audio_output_dir, prefix, f"{prefix}_combined.wav")


#Later
#TODO: Combine the converted chapters into one audio file with limit of 4 hours


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: create an interface for the whole project to make it easier to use
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling