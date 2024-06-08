import PyPDF2
import os

def extract_text_from_pdf(pdf_path, output_txt_path, start, end):
    """"convert the pdf file to one piece of text"""
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Create a text file for output
        with open(output_txt_path, "w") as output_file:
            # Extract text from each page and write it to the text file
            for page_num in range(start, end):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text = text.replace('\t', ' ').replace('\n', ' ').replace('  ', ' ')
                    output_file.write(text + "\n")
                else:
                    print(f"No text found on page {page_num + 1}")


def chapters_generator(text_file, content_list, output_dir):
    """dividing the text file into chapter files in a dedicated folder"""
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    chapters = {}
    for i, (chapter, start_keyword) in enumerate(content_list):
        chapters[chapter] = []
        start_index = None
        end_index = None

        # Find the start index of the current chapter
        for index, line in enumerate(lines):
            if start_keyword in line:
                start_index = index
                break
        # If start index is not found, skip this chapter
        if start_index is None:
            print(f"Start keyword '{start_keyword}' not found for chapter '{chapter}'")
            continue

        # Find the end index of the current chapter
        if i + 1 < len(content_list):
            next_start_keyword = content_list[i + 1][1]
            for index in range(start_index + 1, len(lines)):
                if next_start_keyword in lines[index]:
                    end_index = index
                    break
        else:
            end_index = len(lines)

        # Collect lines for the current chapter
        chapters[chapter] = lines[start_index:end_index]
    
    # Save each chapter to a separate file
    for chapter, chapter_lines in chapters.items():
        output_txt = f"ch{chapter}.txt"
        output_txt = os.path.join(output_dir, f"{chapter}.txt")
        with open(output_txt, 'w', encoding='utf-8') as file:
            file.writelines(chapter_lines)
        print(f"Chapter '{chapter}' saved as {output_txt}")
    

if __name__ == "__main__":
    pdf_path = "mastery/Mastery by Robert Greene.pdf"  # Path to your PDF file
    txt_path = "mastery/Mastery.txt"  # Path for the output text file
    output_dir = "mastery"
    from_page = 17
    to_page = 357

    content_list = [
    ('Introduction', 'THE ULTIMATE POWER'),
    ('Chapter 1', 'DISCOVER YOUR CALLING: THE LIFE’S TASK'),
    ('Chapter 2', 'SUBMIT TO REALITY: THE IDEAL APPRENTICESHIP'),
    ('Chapter 3', 'ABSORB THE MASTER’S POWER: THE MENTOR DYNAMIC'),
    ('Chapter 4', 'SEE PEOPLE AS THEY ARE: SOCIAL INTELLIGENCE'),
    ('Chapter 5', 'AWAKEN THE DIMENSIONAL MIND: THE CREATIVE-ACTIVE'),
    ('Chapter 6', 'FUSE THE INTUITIVE WITH THE RATIONAL: MASTERY'),
    ('Chapter 7', 'CONTEMPORARY MASTER BIOGRAPHIES')
    ]

    extract_text_from_pdf(pdf_path, txt_path, from_page, to_page)

    # Extract chapters based on the content list
    chapters_generator(txt_path, content_list, output_dir)





#DONE: convert the pdf file into a piece of text
#DONE: clean the text from extra spaces
#DONE: divide into chapters to be easier for the model to divide them into chunks for better quality
#DONE: read each chapter by dividing them into chunks and create the audio pieces
#DONE: combine all audio pieces into one

#Later
#TODO: Combine the converted chapters into one audio file with limit of 4 hours


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: create an interface for the whole project to make it easier to use
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling