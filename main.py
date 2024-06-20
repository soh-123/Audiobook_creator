from audio_convert import extract_text_from_pdf, chapters_generator
from audio_convert import chunk_converter, combine_chunks

if __name__ == "__main__":
    pdf_path = "./book.pdf"  # Path to the input PDF book
    txt_path = "./book.txt"  # Path to the output text book
    output_dir = "./book-folder" #Path to the book folder 
    from_page = 15 #start page
    to_page = 782 #end page

    #Enter chapters manually to be divided
    content_list = [
    ('Introduction', 'PREFACE'),
    ('Ch1', 'Chapter 1'),
    ('Ch2', 'Chapter 2'),
    ('Ch3', 'Chapter 3'),
    ('Ch4', 'Chapter 4'),
    ('Ch5', 'Chapter 5'),
    ]

    extract_text_from_pdf(pdf_path, txt_path, from_page, to_page)
    chapters_generator(txt_path, content_list, output_dir)


    textfile_path = "./book-folder/ch1" #converting chapter per chapter
    speaker_voice = "Djano.mp3" #speaker name
    audio_output_dir = "/audio-folder" #path to the audio output
    prefix = "ch1"  # Example prefix for chapter 1
    
    chunk_converter(textfile_path, speaker_voice, audio_output_dir, prefix)
    combine_chunks(audio_output_dir, prefix, f"{prefix}_combined.wav")


#Later
#TODO: Combine the converted chapters into one audio file with limit of 4 hours


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: create an interface for the whole project to make it easier to use
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling