import requests
from dotenv import load_dotenv
import os
import sys
from pypdf import PdfReader

class PDFProcessor:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("LANDING_AI_URL")
        self.api_key = os.getenv("LANDING_AI_API_KEY")
        
    def convert_to_markdown(self, json_response):
        """Convert JSON response to markdown format without saving to file
        
        Args:
            json_response (dict): JSON response from Landing AI API
            
        Returns:
            str: Generated markdown content or None if error occurs
        """
        try:
            from langchain_groq import ChatGroq
            import re
            
            # Initialize LLM
            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model_name="deepseek-r1-distill-llama-70b"
            )
            
            # Create prompt for markdown conversion
            prompt = f"""Convert the following content into a well-structured markdown format while preserving the original information and technical details. Translate the content to Spanish while keeping technical terms in English:

Guidelines:
- Maintain all technical terms (like 'deep learning', 'embedding'), numbers, and mathematical formulas in English exactly as they appear
- Translate all non-technical content to Spanish
- Preserve the hierarchical structure of the content
- Use appropriate markdown syntax for:
  * Headers (using #, ##, ###)
  * Lists (using - or * for bullets)
  * Code blocks (using ```)
  * Mathematical equations (using $ or $$)
- Keep all references and citations in their original format
- Ensure the output is wrapped in ```markdown and ``` tags

Content to format:
{json_response}"""
            
            # Get response from LLM
            raw_response = llm.invoke(prompt)
            message_content = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
            
            # Extract markdown content
            pattern = r'```markdown\n(.+?)\n```'
            match = re.search(pattern, message_content, re.DOTALL)
            if match:
                return match.group(1).strip()
            return message_content
            
        except Exception as e:
            print(f"Error generating markdown: {str(e)}")
            return None

    def process_pdf(self, pdf_path):
        """
        Process a PDF file and convert it using the Landing AI API
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: JSON response from the API
        """
        try:
            files = {
                "pdf": open(pdf_path, "rb")
            }
            
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "X-Include-Marginalia": "false",
                "X-Include-Metadata-In-Markdown": "false"
            }
            
            response = requests.post(self.url, files=files, headers=headers)
            if response.status_code != 200:
                print(f"Error: API request failed with status code {response.status_code}")
                return None
                
            try:
                return response.json()
            except ValueError as e:
                print(f"Error: Invalid JSON response from API: {str(e)}")
                print(f"Response content: {response.text}")
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
