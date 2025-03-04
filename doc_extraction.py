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
            
            response = requests.post(self.url, files=files, headers=headers)
            
            # Check if the request was successful
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
            print(f"API request error: {str(re)}")
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
