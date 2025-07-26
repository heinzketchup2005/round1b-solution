import logging
import numpy as np
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SectionExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def extract_relevant_sections(self, documents: List[Dict], persona_requirements: Dict) -> Dict:
        """Extract and rank relevant sections based on persona requirements"""
        try:
            all_sections = []
            
            # Collect all sections from all documents
            for doc in documents:
                for section in doc['content']:
                    section['document'] = doc['filename']
                    all_sections.append(section)
            
            if not all_sections:
                return {"sections": [], "subsections": []}
            
            # Prepare texts for TF-IDF
            section_texts = [section['content'] for section in all_sections]
            persona_text = persona_requirements['combined_text']
            
            # Add persona text to the corpus for TF-IDF fitting
            all_texts = section_texts + [persona_text]
            
            # Fit TF-IDF and transform
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Get persona vector (last item)
            persona_vector = tfidf_matrix[-1]
            section_vectors = tfidf_matrix[:-1]
            
            # Calculate cosine similarity
            similarities = cosine_similarity(persona_vector, section_vectors)[0]
            
            # Add similarity scores and keyword matches
            key_terms = persona_requirements.get('key_terms', [])
            for i, section in enumerate(all_sections):
                section['relevance_score'] = float(similarities[i])
                
                # Boost score for keyword matches
                keyword_boost = sum(1 for term in key_terms if term.lower() in section['content'].lower())
                section['relevance_score'] += keyword_boost * 0.1
            
            # Sort by relevance
            all_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Select top sections
            top_sections = all_sections[:20]
            
            # Format sections output
            sections_output = []
            for i, section in enumerate(top_sections):
                sections_output.append({
                    "document": section['document'],
                    "page_number": section['page'],
                    "section_title": section['section_title'],
                    "importance_rank": i + 1
                })
            
            # Generate subsections analysis
            subsections_output = self._generate_subsections(
                top_sections[:10], persona_requirements
            )
            
            return {
                "sections": sections_output,
                "subsections": subsections_output
            }
        
        except Exception as e:
            self.logger.error(f"Error extracting sections: {str(e)}")
            return {"sections": [], "subsections": []}
    
    def _generate_subsections(self, sections: List[Dict], persona_requirements: Dict) -> List[Dict]:
        """Generate detailed subsection analysis"""
        subsections = []
        key_terms = persona_requirements.get('key_terms', [])
        
        for section in sections:
            content = section['content']
            
            # Split into sentences
            sentences = content.split('. ')
            
            # Find most relevant sentences
            relevant_sentences = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                relevance_score = sum(1 for term in key_terms if term in sentence_lower)
                
                if relevance_score > 0 or len(relevant_sentences) < 3:
                    relevant_sentences.append(sentence)
            
            # Create refined text
            refined_text = '. '.join(relevant_sentences[:5])  # Max 5 sentences
            
            if refined_text:
                subsections.append({
                    "document": section['document'],
                    "section_title": section['section_title'],
                    "refined_text": refined_text,
                    "page_number": section['page']
                })
        
        return subsections