import fitz
import os

def pdf_to_chapters(pdf_path, start, end, content_list, output_dir):
    """"convert the pdf file into one piece of text"""
    
    # Extract text from the PDF file
    doc = fitz.open(pdf_path)
        
    with open(f"{output_dir}/output.txt", "w", encoding="utf-8") as output_file:
        for page_num in range(start-1, end):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                text = ' '.join(text.splitlines()).replace('  ', ' ')
                output_file.write(text + "\n")
            else:
                print(f"No text found on page {page_num + 1}")

    # Read the content of the text file
    with open(f"{output_dir}/output.txt", 'r', encoding='utf-8') as file:
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
        output_txt = os.path.join(output_dir, f"{chapter}.txt")
        with open(output_txt, 'w', encoding='utf-8') as file:
            file.writelines(chlines)
        print(f"Chapter '{chapter}' saved as {output_txt}")


if __name__ == "__main__":
    pdf_path = "/Users/sohierelsafty/Downloads/How to Own Your Own Mind ( PDFDrive ).pdf"  # Path to the input PDF book
    output_dir = "/Users/sohierelsafty/Desktop/how to own your own mind" #Path to the book folder 
    from_page = 5 #start page
    to_page = 183 #end page

    #Enter chapters manually to be divided
    content_list = [
    ('Ch0', 'Introduction to How to Own Your Own Mind'),
    ('Ch1', 'CHAPTER ONE Creative Vision'),
    ('Ch2', 'Now, let us go back to the question as to how Mr. Edison came to think of'),
    ('Ch3', 'Will you now cite some other examples of the practical application of imagination?'),
    ]

    pdf_to_chapters(pdf_path=pdf_path, output_dir=output_dir, start=from_page, end=to_page, content_list=content_list)
