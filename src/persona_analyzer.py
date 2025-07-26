import logging
import nltk
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class PersonaAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Domain-specific keywords
        self.domain_keywords = {
            'academic': ['research', 'study', 'analysis', 'methodology', 'literature', 'paper', 'journal'],
            'business': ['revenue', 'profit', 'market', 'strategy', 'investment', 'financial', 'growth'],
            'technical': ['implementation', 'algorithm', 'system', 'performance', 'optimization', 'architecture'],
            'educational': ['learning', 'concept', 'understanding', 'exam', 'knowledge', 'study', 'practice']
        }
    
    def analyze_persona_and_job(self, persona: str, job_to_be_done: str) -> Dict:
        """Analyze persona and job to extract requirements"""
        try:
            # Extract key information
            from nltk.tokenize import word_tokenize, sent_tokenize
            import nltk
            nltk.download('punkt', quiet=True)

            # Fallback tokenize manually
            persona_tokens = word_tokenize(persona.lower())
            job_tokens = word_tokenize(job_to_be_done.lower())

            
            # Identify domain
            domain = self._identify_domain(persona, job_to_be_done)
            
            # Extract key terms
            key_terms = self._extract_key_terms(persona, job_to_be_done)
            
            # Create TF-IDF vector for the combined text
            combined_text = f"{persona} {job_to_be_done}"
            
            return {
                'domain': domain,
                'key_terms': key_terms,
                'combined_text': combined_text,
                'persona_type': self._classify_persona_type(persona),
                'task_type': self._classify_task_type(job_to_be_done)
            }
        
        except Exception as e:
            self.logger.error(f"Error analyzing persona: {str(e)}")
            return {}
    
    def _identify_domain(self, persona: str, job: str) -> str:
        """Identify the domain based on persona and job"""
        text = f"{persona} {job}".lower()
        
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            domain_scores[domain] = score
        
        return max(domain_scores, key=domain_scores.get) if domain_scores else 'general'
    
    def _extract_key_terms(self, persona: str, job: str) -> List[str]:
        """Extract important terms from persona and job description"""
        import re
        from nltk.corpus import stopwords
        
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'])
        
        text = f"{persona} {job}".lower()
        
        # Extract meaningful terms
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        key_terms = [word for word in words if word not in stop_words]
        
        # Return most frequent terms
        from collections import Counter
        term_counts = Counter(key_terms)
        return [term for term, count in term_counts.most_common(10)]
    
    def _classify_persona_type(self, persona: str) -> str:
        """Classify the type of persona"""
        persona_lower = persona.lower()
        
        if any(word in persona_lower for word in ['researcher', 'phd', 'scientist']):
            return 'researcher'
        elif any(word in persona_lower for word in ['student', 'undergraduate', 'graduate']):
            return 'student'
        elif any(word in persona_lower for word in ['analyst', 'business', 'investment']):
            return 'analyst'
        elif any(word in persona_lower for word in ['manager', 'executive', 'director']):
            return 'executive'
        else:
            return 'professional'
    
    def _classify_task_type(self, job: str) -> str:
        """Classify the type of task"""
        job_lower = job.lower()
        
        if any(word in job_lower for word in ['review', 'literature', 'survey']):
            return 'review'
        elif any(word in job_lower for word in ['analyze', 'analysis']):
            return 'analysis'
        elif any(word in job_lower for word in ['summarize', 'summary']):
            return 'summary'
        elif any(word in job_lower for word in ['prepare', 'study', 'exam']):
            return 'preparation'
        else:
            return 'general'