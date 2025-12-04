"""Fact-checking layer."""

import re
from typing import List, Dict
from .document_loaders import Document


class FactChecker:
    def __init__(self, docs: List[Document]):
        self.docs = docs
    
    def check_blog_post(self, content: str) -> Dict:
        issues = []
        citations = self._extract_citations(content)
        
        for citation in citations:
            if not self._citation_exists(citation):
                issues.append({
                    'type': 'invalid_citation',
                    'citation': citation,
                    'severity': 'medium'
                })
        
        potential_claims = self._find_claims(content)
        uncited = []
        for claim in potential_claims:
            if not self._has_nearby_citation(content, claim):
                if not self._verify_claim(claim):
                    uncited.append(claim)
        
        if uncited:
            issues.append({
                'type': 'uncited_claims',
                'claims': uncited[:5],
                'severity': 'low'
            })
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues,
            'citation_count': len(citations)
        }
    
    def check_tweet_ideas(self, tweets: List[Dict[str, str]]) -> Dict:
        issues = []
        missing_sources = []
        
        for i, tweet in enumerate(tweets):
            text = tweet.get('tweet', '')
            source = tweet.get('source', '')
            
            if self._has_specific_claim(text) and not source:
                missing_sources.append({
                    'index': i + 1,
                    'tweet': text[:100] + '...' if len(text) > 100 else text
                })
        
        if missing_sources:
            issues.append({
                'type': 'tweets_missing_sources',
                'tweets': missing_sources,
                'severity': 'low'
            })
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues
        }
    
    def _extract_citations(self, content: str) -> List[str]:
        return re.findall(r'\[Source:\s*([^\]]+)\]', content)
    
    def _citation_exists(self, citation: str) -> bool:
        citation_lower = citation.lower()
        for doc in self.docs:
            if citation_lower in doc.title.lower() or citation_lower in doc.source.lower():
                return True
        return False
    
    def _find_claims(self, content: str) -> List[str]:
        sentences = re.split(r'[.!?]+', content)
        claims = []
        
        patterns = [
            r'\d+%',
            r'\$\d+',
            r'\d+\s*(million|billion|thousand)',
            r'(increased|decreased|rose|fell|grew|shrank)',
            r'(according to|data shows|research indicates)'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                for pattern in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        claims.append(sentence[:200])
                        break
        
        return claims
    
    def _has_nearby_citation(self, content: str, claim: str) -> bool:
        pos = content.find(claim)
        if pos == -1:
            return False
        
        start = max(0, pos - 100)
        end = min(len(content), pos + len(claim) + 100)
        nearby = content[start:end]
        
        return bool(re.search(r'\[Source:', nearby))
    
    def _verify_claim(self, claim: str) -> bool:
        terms = re.findall(r'\b\w{4,}\b', claim.lower())
        if not terms:
            return False
        
        for doc in self.docs:
            doc_lower = doc.content.lower()
            matches = sum(1 for term in terms[:5] if term in doc_lower)
            if matches >= 2:
                return True
        
        return False
    
    def _has_specific_claim(self, text: str) -> bool:
        patterns = [
            r'\d+%',
            r'\$\d+',
            r'\d+\s*(million|billion|thousand)',
            r'(is|are|was|were)\s+(up|down|increasing|decreasing)'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
