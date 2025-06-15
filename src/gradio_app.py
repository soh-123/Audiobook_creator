import gradio as gr
from src.pdf_splitter import pdf_to_chapters
from src.capCut import gradio_callback
from src.audio_convert import audio_converter


def display_gallery(history):
    # Display all generated audios in the current session.
    audio_boxes = []
    for i, (label, wav_path) in enumerate(history):
        audio_boxes.append(gr.Audio(wav_path, label=f"{label}"))
    return audio_boxes

with gr.Blocks() as demo:
    gr.Markdown("# Audiobook to Video Creator")

    with gr.Tabs():
        # Step 1: PDF to Chapters
        with gr.TabItem("1. Split PDF to Chapters"):
            gr.Markdown("### Upload your PDF book and split it into chapters.")
            pdf_input = gr.File(label="Upload PDF")
            from_page = gr.Number(label="Start Page", value=1)
            to_page = gr.Number(label="End Page", value=10)
            chapters_df = gr.Dataframe(
                headers=["chapter", "keyword"],
                datatype=["str", "str"],
                row_count=3,
                col_count=(2, "fixed"),
                value=[["Ch0", ""], ["Ch1", ""], ["Ch2", ""]]
            )
            split_btn = gr.Button("Split PDF")
            chapters_list = gr.Dataframe(
                headers=["Chapter File", "Download Link"],
                value=[],
                interactive=False
            )
            split_btn.click(
                pdf_to_chapters, 
                inputs=[pdf_input, from_page, to_page, chapters_df], 
                outputs=chapters_list
            )

        # Step 2: Text to Audio
        with gr.TabItem("2. Convert Chapter to Audio"):
            gr.Markdown("### Upload a chapter text file OR write/paste text, then generate audio. Repeat for as many as you want.")
            
            txt_input = gr.File(label="Upload Reviewed Text File (.txt)")
            text_area = gr.Textbox(label="Or write/paste short text", lines=4, placeholder="Paste a paragraph or write your own")
            voice_input = gr.File(label="Upload Voice File (wav/mp3)")
            convert_btn = gr.Button("Convert to Audio")
            error_box = gr.Markdown()
            audio_gallery = gr.Column()
            session_history = gr.State([])

            convert_btn.click(
                audio_converter,
                inputs=[txt_input, text_area, voice_input, session_history],
                outputs=[session_history, error_box]
            ).then(
                display_gallery,
                inputs=session_history,
                outputs=audio_gallery
            )

        # Step 3: Combine & Video
        with gr.TabItem("3. Combine Audio & Create Video"):
            gr.Markdown("### Upload all audio files in order and a cover image, then generate your final video.")
            audio_files = gr.Files(label="Upload All Chapter Audios (.wav)", file_types=["audio"])
            cover_image = gr.Image(label="Upload Cover Image")
            generate_video_btn = gr.Button("Generate Video")
            video_output = gr.Video(label="Final MP4 Video")
            generate_video_btn.click(gradio_callback, [audio_files, cover_image], video_output) # To be implemented

    gr.Markdown("> **Tip:** Complete each step before moving to the next for the best results.")

demo.launch(share=True)
