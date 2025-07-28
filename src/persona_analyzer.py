import logging
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from collections import Counter

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
            # Minimal tokenizer fallback (no NLTK required)
            persona_tokens = self._simple_tokenize(persona)
            job_tokens = self._simple_tokenize(job_to_be_done)

            domain = self._identify_domain(persona, job_to_be_done)
            key_terms = self._extract_key_terms(persona, job_to_be_done)
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

    def _simple_tokenize(self, text: str) -> List[str]:
        """Very basic word tokenizer that avoids NLTK dependency"""
        return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

    def _identify_domain(self, persona: str, job: str) -> str:
        """Identify the domain based on persona and job"""
        text = f"{persona} {job}".lower()
        domain_scores = {
            domain: sum(1 for keyword in keywords if keyword in text)
            for domain, keywords in self.domain_keywords.items()
        }
        return max(domain_scores, key=domain_scores.get) if domain_scores else 'general'

    def _extract_key_terms(self, persona: str, job: str) -> List[str]:
        """Extract important terms from persona and job description"""
        stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'as', 'by', 'is', 'it', 'that', 'this'
        ])
        text = f"{persona} {job}".lower()
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        key_terms = [word for word in words if word not in stop_words]
        term_counts = Counter(key_terms)
        return [term for term, count in term_counts.most_common(10)]

    def _classify_persona_type(self, persona: str) -> str:
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
