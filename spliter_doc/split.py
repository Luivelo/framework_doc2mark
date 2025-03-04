import os
from pypdf import PdfReader, PdfWriter
from pathlib import Path

def split_pdf_into_pages():
    """
    Splits each PDF in the original_docs directory into individual pages
    and saves each page as a separate PDF file in the splitted_docs directory.
    """
    # Define paths using relative paths
    current_dir = Path(__file__).parent
    original_docs_path = (current_dir / ".." / "original_docs").resolve()
    output_path = (current_dir / "splitted_docs").resolve()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Get all PDF files from the original_docs directory
    pdf_files = [f for f in os.listdir(original_docs_path) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        input_pdf_path = os.path.join(original_docs_path, pdf_file)
        
        # Open the PDF file
        with open(input_pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # Extract the filename without extension
            filename_base = os.path.splitext(pdf_file)[0]
            
            # Process each page
            for page_num in range(total_pages):
                # Create a PDF writer object for the output file
                pdf_writer = PdfWriter()
                
                # Add the current page to the writer
                pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Create output filename for this page
                output_filename = f"{filename_base}_page_{page_num+1}.pdf"
                output_file_path = os.path.join(output_path, output_filename)
                
                # Write the page to a new PDF file
                with open(output_file_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                print(f"Created: {output_filename}")
    
    print(f"All PDFs have been split into individual pages in: {output_path}")

if __name__ == "__main__":
    split_pdf_into_pages()
