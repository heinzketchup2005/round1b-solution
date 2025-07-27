# Round 1B: Persona-Driven Document Intelligence

 ## Overview
This solution implements a persona-driven document intelligence system that extracts and ranks relevant sections from document collections based on specific persona requirements and task objectives.

## Approach
1. **PDF Processing**: Extract structured content from PDFs with page numbers and section titles
2. **Persona Analysis**: Analyze persona and job requirements to identify domain and extract key terms
3. **Semantic Matching**: Utilize sentence transformers to identify semantically similar content
4. **Section Ranking**: Rank sections based on relevance to persona requirements
5. **Subsection Analysis**: Extract and refine the most relevant text portions

## Models and Dependencies
- **Sentence Transformers**: all-MiniLM-L6-v2 (80MB) for semantic similarity
- **NLTK**: For text preprocessing and tokenization
- **scikit-learn**: For TF-IDF vectorization and cosine similarity calculations
- **PyPDF2 & pdfplumber**: For PDF text extraction
- **NumPy**: For numerical operations

## Building and Running

### Build Docker Image
```bash
docker build --platform linux/amd64 -t persona-doc-intelligence:v1 .
```

### Run Solution
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  persona-doc-intelligence:v1
```

## Input Structure
```
input/
├── documents/
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
├── persona.txt
└── job_to_be_done.txt
```

### Example Persona
```
PhD Researcher in Computational Biology specializing in machine learning 
for drug discovery. Has expertise in graph neural networks, molecular 
modeling, and bioinformatics. Focuses on methodological innovation 
and performance benchmarking.
```

### Example Job-to-be-Done
```
Prepare a comprehensive literature review focusing on methodologies, 
datasets, and performance benchmarks for Graph Neural Networks in 
Drug Discovery. Need to identify key approaches, compare different 
methods, and summarize experimental results.
```

## Output
The solution generates `challenge1b_output.json` with:
- Metadata about input documents, persona, and job
- Ranked relevant sections with importance scores
- Detailed subsection analysis with refined text

## Performance
- **Model Size**: <200MB total (all-MiniLM-L6-v2 is only 80MB)
- **Processing Time**: <60 seconds for 3-5 documents
- **Hardware Requirements**: CPU-only execution on AMD64 architecture
- **Network**: No internet connection required during execution

## Project Structure
```
.
├── Dockerfile                # Container definition for the solution
├── README.md                # This file
├── approach_explanation.md  # Detailed explanation of the approach
├── input/                   # Input directory for documents and requirements
├── models/                  # Directory for model files
│   └── download_models.py   # Script to download required models
├── output/                  # Output directory for results
├── requirements.txt         # Python dependencies
└── src/                     # Source code
    ├── __init__.py
    ├── main.py              # Main entry point
    ├── pdf_processor.py     # PDF extraction and processing
    ├── persona_analyzer.py  # Persona and job analysis
    ├── section_extractor.py # Section extraction and ranking
    └── utils.py             # Utility functions
```

## Implementation Details

### PDF Processing
The `PDFProcessor` class extracts text from PDF documents while preserving page numbers and attempting to infer section titles. It uses pdfplumber for robust text extraction and structures the content into sections.

### Persona Analysis
The `PersonaAnalyzer` class analyzes the persona and job descriptions to identify the domain, extract key terms, and classify the persona type. This information is used to guide the section extraction process.

### Section Extraction
The `SectionExtractor` class ranks document sections based on their relevance to the persona requirements. It uses TF-IDF vectorization and cosine similarity to calculate relevance scores, and applies domain-specific boosts for keyword matches.

## Detailed Approach

For a more detailed explanation of the approach, methodology, and technical decisions, please refer to the [approach_explanation.md](approach_explanation.md) file.

## Future Improvements

- Implement more advanced section title extraction using machine learning
- Add support for more document formats beyond PDF
- Incorporate domain-specific knowledge graphs for better relevance scoring
- Implement cross-document reference linking for more comprehensive analysis
- Add visualization capabilities for section relevance and relationships