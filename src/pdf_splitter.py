import fitz
import os
import tempfile

def pdf_to_chapters(pdf_file, from_page, to_page, chapters_df):
    """
    Splitting a PDF into chapter .txt files.
    Args:
        pdf_file: Uploaded PDF (Gradio File object)
        from_page: Start page (int)
        to_page: End page (int)
        chapters_df: DataFrame value as list of dicts, e.g. [{"chapter": "Ch0", "keyword": "Intro"}, ...]
    Returns:
        List of (chapter file name, file path) for Gradio Dataframe or file downloads.
    """
    
    # Save PDF to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "book.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        output_txt = os.path.join(tmpdir, "output.txt")

    # Extract text from the PDF file
    doc = fitz.open(pdf_file)
    with open(output_txt, "w", encoding="utf-8") as output_file:
        for page_num in range(int(from_page) - 1, int(to_page)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                text = ' '.join(text.splitlines()).replace('  ', ' ')
                output_file.write(text + "\n")
            else:
                print(f"No text found on page {page_num + 1}")

    # Read the content of the text file
    with open(output_txt, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each chapter based on the content list
    chapters = {}
    content_list = [(row["chapter"], row["keyword"]) for row in chapters_df if row["chapter"] and row["keyword"]]

    for i, (chapter, start_keyword) in enumerate(content_list):
        chapters[chapter] = []
        start_index = None
        end_index = None

        # Find the start index of the current chapter
        for index, line in enumerate(lines):
            if start_keyword in line:
                start_index = index
                break 
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
        chapters[chapter] = lines[start_index:end_index]

    # Save each chapter to a separate file
    result = []
    for chapter, chlines in chapters.items():
        chapter_txt = os.path.join(tmpdir, f"{chapter}.txt")
        with open(chapter_txt, 'w', encoding='utf-8') as file:
            file.writelines(chlines)
        result.append((f"{chapter}.txt", chapter_txt))
    return result
