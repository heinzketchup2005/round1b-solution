# Round 1B: Persona-Driven Document Intelligence

## Overview
This solution builds an intelligent document analyst that extracts and prioritizes the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

## Approach
1. **PDF Processing**: Extract structured content from PDFs with page numbers and section titles
2. **Persona Analysis**: Analyze persona and job requirements to understand domain and key terms
3. **Semantic Matching**: Use sentence transformers to find semantically similar content
4. **Section Ranking**: Rank sections based on relevance to persona requirements
5. **Subsection Analysis**: Extract and refine the most relevant text portions

## Models Used
- **Sentence Transformers**: all-MiniLM-L6-v2 (80MB) for semantic similarity
- **NLTK**: For text preprocessing and tokenization
- **spaCy**: For natural language processing

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

## Output
The solution generates `challenge1b_output.json` with:
- Metadata about input documents, persona, and job
- Ranked relevant sections with importance scores
- Detailed subsection analysis with refined text

## Performance
- Model size: <200MB
- Processing time: <60 seconds for 3-5 documents
- CPU-only execution on AMD64 architecture