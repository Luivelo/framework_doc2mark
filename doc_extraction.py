import requests
from dotenv import load_dotenv
import os
import json

class PDFProcessor:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("LANDING_AI_URL")
        self.api_key = os.getenv("LANDING_AI_API_KEY")

    def process_pdf(self, pdf_path):
        """
        Process a PDF file and convert it using the Landing AI API
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: JSON response from the API
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            files = {
                "pdf": open(pdf_path, "rb")
            }
            
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "X-Include-Marginalia": "false",
                "X-Include-Metadata-In-Markdown": "false"
            }
            
            # Validate PDF file size and format before sending
            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                raise ValueError("PDF file is empty")
            
            response = requests.post(self.url, files=files, headers=headers)
            
            # Check response status and provide detailed error messages
            if response.status_code == 422:
                error_detail = response.json().get('detail', 'Unknown error')
                raise requests.exceptions.HTTPError(
                    f"PDF processing failed (422): {error_detail}. "
                    "Please ensure the PDF is valid and not corrupted."
                )
            response.raise_for_status()
            
            # Validate JSON response
            try:
                json_response = response.json()
                if not json_response:
                    raise ValueError("Empty response from API")
                return json_response
            except json.JSONDecodeError as je:
                print(f"Invalid JSON response: {str(je)}")
                print(f"Response content: {response.text}")
                return None
            
        except requests.exceptions.RequestException as re:
            error_msg = f"API request error: {str(re)}"
            if response.status_code == 422:
                error_msg += "\nPossible causes:\n- PDF file may be corrupted\n- File format not supported\n- File size too large"
            print(error_msg)
            return None
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
        finally:
            if 'files' in locals() and 'pdf' in files:
                files['pdf'].close()

# Example usage:
# processor = PDFProcessor()
# result = processor.process_pdf("spliter_doc/splitted_docs/2502.01143v2_page_10.pdf")
# print(result)
