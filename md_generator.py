import os
import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from doc_extraction import PDFProcessor

def init_llm():
    """Initialize the Groq LLM with environment variables
    
    Returns:
        ChatGroq: Initialized LLM instance
    """
    load_dotenv()
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="deepseek-r1-distill-llama-70b"
    )

def create_markdown_prompt(json_response):
    """Create a prompt for markdown conversion with language specifications
    
    Args:
        json_response (dict): JSON response from Landing AI API
        
    Returns:
        str: Formatted prompt for the LLM
    """
    prompt_template = PromptTemplate(
        input_variables=["content"],
        template="""Convert the following content into a well-structured markdown format while preserving the original information and technical details. Translate the content to Spanish while keeping technical terms in English:

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
- Keep tables info, their contents, and abbreviations in English
- Ensure the output is wrapped in ```markdown and ``` tags

Content to format:
{content}"""
    )
    return prompt_template.format(content=json_response)

def extract_markdown_content(llm_response):
    """Extract markdown content from between code blocks
    
    Args:
        llm_response (str): Raw response from LLM
        
    Returns:
        str: Extracted markdown content
    """
    pattern = r'```markdown\n(.+?)\n```'
    match = re.search(pattern, llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response

def save_markdown(content, output_path):
    """Save markdown content to file
    
    Args:
        content (str): Markdown content to save
        output_path (str): Path to save the markdown file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Markdown file saved successfully at: {output_path}")

def process_json_to_markdown(json_response, output_path=None):
    """Convert JSON response to markdown format using Groq LLM
    
    Args:
        json_response (dict): JSON response from Landing AI API
        output_path (str, optional): Path to save the markdown file. If None, only returns the content
        
    Returns:
        str: Generated markdown content or None if error occurs
    """
    try:
        llm = init_llm()
        prompt = create_markdown_prompt(json_response)
        raw_response = llm.invoke(prompt)
        # Extract content from AIMessage object
        message_content = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
        markdown_content = extract_markdown_content(message_content)
        
        if output_path:
            save_markdown(markdown_content, output_path)
            
        return markdown_content
    except Exception as e:
        print(f"Error generating markdown: {str(e)}")
        return None

# # Example usage:
# processor = PDFProcessor()
# result = processor.process_pdf("spliter_doc/splitted_docs/2502.20396v1_page_3.pdf")
# markdown_content = process_json_to_markdown(
#     result,
#     "spliter_doc/md_docs/output_2.md"
# )
