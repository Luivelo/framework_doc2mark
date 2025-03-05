import streamlit as st
import os
import tempfile
import base64
from doc_extraction import PDFProcessor
from md_generator import process_json_to_markdown, TextGenerator
from text2speech import text_to_speech
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    page_title="PDF to Markdown Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .markdown-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        background-color: #f9f9f9;
        height: auto;
        min-height: 400px;
        width: 100%;
        box-sizing: border-box;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    .preview-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        background-color: white;
        height: auto;
        min-height: 400px;
        width: 100%;
        box-sizing: border-box;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    .stMarkdown {
        margin-top: 0;
        margin-bottom: 1rem;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    .copy-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 14px;
        cursor: pointer;
        margin-right: 10px;
        display: inline-block;
    }
    .copy-button:hover {
        background-color: #45a049;
    }
    .button-container {
        display: flex;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .stCodeBlock {
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">PDF to Markdown Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert your PDF documents to Markdown format with audio support</p>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Process the PDF
    processor = PDFProcessor()
    result = processor.process_pdf(tmp_file_path)

    if result:
        # Generate markdown content
        markdown_content = process_json_to_markdown(result)

        # Generate text content for speech
        text_generator = TextGenerator()
        text_content = text_generator.generate_text(result)

        if text_content:
            # Generate audio
            audio_path = text_to_speech(text_content)
            
            if audio_path:
                # Audio player section with aesthetic title
                st.markdown('<h2 class="sub-header" style="text-align: center; margin-top: 2rem;">🎧 Reproduce para escuchar el Paper</h2>', unsafe_allow_html=True)
                
                # Display audio player
                audio_file = open(audio_path, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                audio_file.close()

        # Display markdown content
        if markdown_content:
            st.markdown('<h2 class="sub-header">Resultado Markdown</h2>', unsafe_allow_html=True)
            
            # Create tabs for code and preview
            code_tab, preview_tab = st.tabs(["Código", "Vista Previa"])
            
            with code_tab:
                st.markdown('<div class="markdown-container">', unsafe_allow_html=True)
                st.code(markdown_content, language='markdown')
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add copy button
                st.markdown(
                    f'''
                    <div class="button-container">
                        <button class="copy-button" onclick="
                            navigator.clipboard.writeText(`{markdown_content}`);
                            this.textContent='¡Copiado!';
                            setTimeout(() => this.textContent='Copiar al Portapapeles', 2000);
                        ">Copiar al Portapapeles</button>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            
            with preview_tab:
                st.markdown('<div class="preview-container">', unsafe_allow_html=True)
                st.markdown(markdown_content)
                st.markdown('</div>', unsafe_allow_html=True)

        # Clean up temporary files
        os.unlink(tmp_file_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.unlink(audio_path)

    else:
        st.error("Error processing the PDF file. Please try again.")

# Footer
st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Streamlit, Landing AI y Groq LLM")

# Cleanup temporary directory when the app is closed
# Note: This might not always execute in Streamlit's execution model
def cleanup():
    temp_dir.cleanup()

# Register the cleanup function
import atexit
atexit.register(cleanup)

# Initialize text generator
text_generator = TextGenerator()

# Process PDF and generate text/markdown
if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        pdf_path = tmp_file.name

    # Process PDF
    processor = PDFProcessor()
    json_response = processor.process_pdf(pdf_path)

    if json_response:
        # Generate text for speech
        text_content = text_generator.generate_text(json_response)
        
        # Generate markdown
        markdown_content = process_json_to_markdown(json_response)

        if markdown_content:
            st.markdown("### Generated Markdown")
            st.text_area("Markdown Content", markdown_content, height=400)

            # Text-to-Speech conversion
            if text_content:
                audio_file = text_to_speech(text_content)
                if audio_file:
                    st.audio(audio_file)

            # Download buttons
            st.download_button(
                label="Download Markdown",
                data=markdown_content,
                file_name="converted.md",
                mime="text/markdown"
            )

    # Clean up temporary file
    os.unlink(pdf_path)

# Cleanup temporary directory when the app is closed
# Note: This might not always execute in Streamlit's execution model
def cleanup():
    temp_dir.cleanup()

# Register the cleanup function
import atexit
atexit.register(cleanup)