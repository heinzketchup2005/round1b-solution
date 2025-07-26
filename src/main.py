import os
import json
import logging
from datetime import datetime
from pdf_processor import PDFProcessor
from persona_analyzer import PersonaAnalyzer
from section_extractor import SectionExtractor

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        pdf_processor = PDFProcessor()
        persona_analyzer = PersonaAnalyzer()
        section_extractor = SectionExtractor()
        
        # Read input files
        input_dir = "/app/input"
        documents_dir = os.path.join(input_dir, "documents")
        
        # Read persona and job description
        with open(os.path.join(input_dir, "persona.txt"), 'r') as f:
            persona = f.read().strip()
        
        with open(os.path.join(input_dir, "job_to_be_done.txt"), 'r') as f:
            job_to_be_done = f.read().strip()
        
        # Process all PDFs
        pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            logger.error("No PDF files found")
            return
        
        logger.info(f"Processing {len(pdf_files)} documents...")
        
        # Extract content from all documents
        all_documents = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(documents_dir, pdf_file)
            document_data = pdf_processor.process_pdf(pdf_path, pdf_file)
            all_documents.append(document_data)
        
        # Analyze persona requirements
        persona_requirements = persona_analyzer.analyze_persona_and_job(persona, job_to_be_done)
        
        # Extract and rank relevant sections
        relevant_sections = section_extractor.extract_relevant_sections(
            all_documents, persona_requirements
        )
        
        # Generate output
        output = {
            "metadata": {
                "input_documents": pdf_files,
                "persona": persona,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": relevant_sections["sections"],
            "subsection_analysis": relevant_sections["subsections"]
        }
        
        # Write output
        output_path = "/app/output/challenge1b_output.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()