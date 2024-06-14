import fitz
import os


#DONE: convert the pdf file into a piece of text
#DONE: clean the text from extra spaces
#DONE: divide into chapters to be easier for the model to divide them into chunks for better quality

def extract_text_from_pdf(pdf_path, output_txt_path, start, end):
    """"convert the pdf file to one piece of text"""
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
        
    # Create a text file for output
    with open(output_txt_path, "w", encoding="utf-8") as output_file:
        for page_num in range(start, end):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                text = text.replace('\t', ' ').replace('\n', ' ').replace('  ', ' ')
                output_file.write(text + "\n")
            else:
                print(f"No text found on page {page_num + 1}")


def chapters_generator(text_file, content_list, output_dir):
    """dividing the text file into chapter files in a dedicated folder"""

    # Read the content of the text file
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    chapters = {}

    # Process each chapter based on the content list
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
    for chapter, chlines in chapters.items():
        output_txt = f"ch{chapter}.txt"
        output_txt = os.path.join(output_dir, f"{chapter}.txt")
        with open(output_txt, 'w', encoding='utf-8') as file:
            file.writelines(chlines)
        print(f"Chapter '{chapter}' saved as {output_txt}")