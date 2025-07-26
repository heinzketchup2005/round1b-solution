import PyPDF2
import pdfplumber
import logging
from typing import Dict, List, Any

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_pdf(self, pdf_path: str, filename: str) -> Dict[str, Any]:
        """Process a PDF and extract structured content"""
        try:
            with open(pdf_path, 'rb') as file:
                # Extract text content
                content = self._extract_text_with_structure(pdf_path)
                
                return {
                    "filename": filename,
                    "content": content
                }
        except Exception as e:
            self.logger.error(f"Error processing {filename}: {str(e)}")
            return {"filename": filename, "content": []}
    
    def _extract_text_with_structure(self, pdf_path: str) -> List[Dict]:
        """Extract text with page and section information"""
        sections = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    # Split into paragraphs
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    
                    for para_idx, paragraph in enumerate(paragraphs):
                        if len(paragraph) > 50:  # Filter out very short paragraphs
                            section_title = self._infer_section_title(paragraph)
                            sections.append({
                                "page": page_num,
                                "section_title": section_title,
                                "content": paragraph,
                                "paragraph_index": para_idx
                            })
        
        return sections
    
    def _infer_section_title(self, paragraph: str) -> str:
        """Infer section title from paragraph content"""
        lines = paragraph.split('\n')
        first_line = lines[0].strip()
        
        # If first line is short and contains key indicators, use as title
        if (len(first_line) < 100 and 
            (first_line.isupper() or 
             any(word in first_line.lower() for word in ['introduction', 'conclusion', 'method', 'result', 'discussion', 'abstract', 'summary']))):
            return first_line
        
        # Otherwise, create a title from first few words
        words = first_line.split()[:8]
        return ' '.join(words) + ('...' if len(first_line.split()) > 8 else '')