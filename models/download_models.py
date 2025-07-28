import nltk
import spacy
from sentence_transformers import SentenceTransformer
import os

def download_models():
    """Download required models for offline processing"""
    print("Downloading NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    
    print("Downloading spaCy models...")
    os.system("python -m spacy download en_core_web_sm")
    
    print("Downloading sentence transformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save('/app/models/sentence_transformer')
    
    print("All models downloaded successfully!")

if __name__ == "__main__":
    download_models()