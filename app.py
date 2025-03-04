import streamlit as st
import os
import tempfile
import base64
from doc_extraction import PDFProcessor
from md_generator import process_json_to_markdown
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
st.markdown('<h1 class="main-header">PDF a Markdown Converter</h1>', unsafe_allow_html=True)
st.markdown('''
    Esta aplicación convierte documentos PDF en formato Markdown estructurado.
    Sube un PDF de 1-2 páginas y obtén el código Markdown generado junto con una vista previa renderizada.
''')

# Create a temporary directory to store uploaded files
temp_dir = tempfile.TemporaryDirectory()

# Function to display PDF
@st.cache_data
def display_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'''
            <div style="width:100%; height:500px; overflow:hidden; border-radius:5px;">
                <embed
                    src="data:application/pdf;base64,{base64_pdf}"
                    type="application/pdf"
                    width="100%"
                    height="100%"
                    style="border:none;"
                />
            </div>
        '''
        return pdf_display
    except Exception as e:
        st.error(f"Error al cargar el PDF: {str(e)}")
        return None

# Main layout with columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="sub-header">Subir PDF</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecciona un archivo PDF (1-2 páginas)", type="pdf")
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_pdf_path = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display the uploaded PDF
        st.markdown("### PDF Subido")
        st.markdown(display_pdf(temp_pdf_path), unsafe_allow_html=True)
        
        # Process button
        if st.button("Convertir a Markdown"):
            with st.spinner("Procesando PDF..."):
                # Process the PDF using the existing framework
                processor = PDFProcessor()
                result = processor.process_pdf(temp_pdf_path)
                
                if result:
                    try:
                        # Process JSON to markdown using md_generator
                        markdown_content = process_json_to_markdown(result)
                        
                        if markdown_content:
                            # Store the markdown content in session state for display
                            st.session_state.markdown_content = markdown_content
                            st.success("¡Conversión completada!")
                        else:
                            st.error("Error al generar el markdown.")
                    except Exception as e:
                        st.error(f"Error durante la conversión: {str(e)}")
                else:
                    st.error("Error al procesar el PDF.")

with col2:
    st.markdown('<h2 class="sub-header">Resultado Markdown</h2>', unsafe_allow_html=True)
    
    # Create tabs for raw markdown and rendered preview
    tab1, tab2 = st.tabs(["Código Markdown", "Vista Previa"])
    
    with tab1:
        if 'markdown_content' in st.session_state:
            # Display the markdown code with syntax highlighting only
            st.code(st.session_state.markdown_content, language="markdown")
            
            # Add download button for markdown
            st.download_button(
                label="Descargar Markdown",
                data=st.session_state.markdown_content,
                file_name="converted_markdown.md",
                mime="text/markdown"
            )
        else:
            st.info("Sube un PDF y haz clic en 'Convertir a Markdown' para ver el resultado.")
    
    with tab2:
        if 'markdown_content' in st.session_state:
            # Direct rendering of markdown with HTML support
            st.markdown(st.session_state.markdown_content, unsafe_allow_html=True)
        else:
            st.info("Sube un PDF y haz clic en 'Convertir a Markdown' para ver la vista previa.")

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