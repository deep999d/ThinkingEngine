"""LLM orchestration for content generation."""

import os
import re
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from .document_loaders import Document

load_dotenv()


class LLMOrchestrator:
    def __init__(self, model: str = None, temperature: float = 0.3):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        self.temperature = temperature
    
    def summarize_documents(self, docs: List[Document]) -> str:
        context = self._build_context(docs)
        
        prompt = f"""You are analyzing a curated set of articles and reports about cryptocurrency, blockchain, and fintech.

Your task is to create a comprehensive summary that:
1. Identifies the main themes and topics across all documents
2. Highlights key insights and data points
3. Notes any contradictions or different perspectives
4. Maintains source attribution for all claims

Documents to analyze:
{context}

Provide a structured summary that will be used to generate original blog content. Focus on facts, data, and verifiable claims from these sources."""

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a careful analyst who only makes claims supported by the provided sources."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return resp.choices[0].message.content
    
    def generate_blog_post(self, docs: List[Document], summary: str) -> str:
        context = self._build_context(docs)
        
        prompt = f"""Based on the following curated research documents, write an original, insightful weekly blog post.

Requirements:
1. Write in a professional, engaging tone suitable for a crypto/fintech audience
2. Develop original perspectives and analysis based on the provided sources
3. Include inline citations in the format [Source: Document Title] for all claims
4. Structure: Headline, Executive Summary (2-3 sentences), Body (multiple sections), Key Takeaways
5. Do NOT make claims not supported by the sources - if unsure, flag it
6. Focus on actionable insights and analysis, not just summary

Research Summary:
{summary}

Source Documents:
{context}

Generate the blog post now:"""

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional crypto/fintech writer. You only make claims supported by your sources and always cite them."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return resp.choices[0].message.content
    
    def generate_tweet_ideas(self, docs: List[Document], summary: str, count: int = 25) -> List[Dict[str, str]]:
        context = self._build_context(docs)
        
        prompt = f"""Based on the following research, generate EXACTLY {count} tweet ideas. Each tweet must be formatted as follows:

TWEET: [the tweet text - under 280 characters]
HASHTAGS: [relevant hashtags and cashtags]
SOURCE: [source document if specific claim]

Requirements:
- Generate EXACTLY {count} tweets (numbered 1 through {count})
- Each tweet should be engaging and shareable
- Based on insights from the provided sources
- Include relevant hashtags (e.g., #Bitcoin, #DeFi, #Web3) and cashtags (e.g., $BTC, $ETH) where appropriate
- Varied in style: some data-driven, some opinion, some questions, some insights
- Each tweet must be under 280 characters
- Use the exact format above for each tweet

Research Summary:
{summary}

Source Documents:
{context}

Now generate {count} tweets in the exact format specified:"""

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a social media strategist creating engaging crypto/fintech content based on research."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature + 0.1
        )
        
        return self._parse_tweets(resp.choices[0].message.content)
    
    def _build_context(self, docs: List[Document]) -> str:
        max_per_doc = int(os.getenv("MAX_CHARS_PER_DOCUMENT", "12000"))
        max_total = int(os.getenv("MAX_TOTAL_CONTEXT_CHARS", "50000"))
        
        parts = []
        total = 0
        truncated = []
        
        for i, doc in enumerate(docs, 1):
            header = f"\n--- Document {i}: {doc.title} (Source: {doc.source}) ---\n"
            header_len = len(header)
            
            remaining = max_total - total - header_len
            if remaining < 1000 and i > 1:
                print(f"⚠️  Warning: Stopping at document {i} to avoid token limits. {len(docs) - i} documents not included.")
                break
            
            content = doc.content
            orig_len = len(content)
            
            if len(content) > max_per_doc:
                start = max_per_doc // 2
                end = max_per_doc - start - 50
                content = (
                    content[:start] + 
                    f"\n\n[... {orig_len - max_per_doc} characters truncated from middle ...]\n\n" +
                    content[-end:]
                )
                truncated.append(doc.title)
            
            if len(content) > remaining:
                start = remaining // 2
                end = remaining - start - 50
                content = (
                    content[:start] + 
                    f"\n\n[... content truncated to fit context limit ...]\n\n" +
                    content[-end:]
                )
            
            parts.append(header)
            parts.append(content)
            parts.append("\n")
            total += header_len + len(content)
        
        if truncated:
            print(f"⚠️  Warning: {len(truncated)} document(s) were truncated: {', '.join(truncated[:3])}")
            if len(truncated) > 3:
                print(f"   ... and {len(truncated) - 3} more")
        
        return "\n".join(parts)
    
    def _parse_tweets(self, text: str) -> List[Dict[str, str]]:
        tweets = []
        current = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current and current.get('tweet'):
                    tweets.append(current)
                    current = {}
                continue
            
            # Handle TWEET: prefix (with or without numbering)
            if 'TWEET:' in line.upper():
                if current and current.get('tweet'):
                    tweets.append(current)
                # Remove numbering and TWEET: prefix
                tweet_text = re.sub(r'^\d+\.\s*', '', line, flags=re.IGNORECASE)
                tweet_text = re.sub(r'^TWEET:\s*', '', tweet_text, flags=re.IGNORECASE)
                current = {'tweet': tweet_text.strip()}
            elif line.upper().startswith('HASHTAGS:'):
                current['hashtags'] = line.replace('HASHTAGS:', '').replace('hashtags:', '').strip()
            elif line.upper().startswith('SOURCE:'):
                current['source'] = line.replace('SOURCE:', '').replace('source:', '').strip()
            elif current.get('tweet'):
                # Continue building tweet if we already have one
                if not current.get('hashtags') and not line.upper().startswith('HASHTAGS'):
                    current['tweet'] += ' ' + line
            elif line and not any(keyword in line.upper() for keyword in ['TWEET:', 'HASHTAGS:', 'SOURCE:']):
                # Start new tweet if line looks like tweet content
                if len(line) > 20:  # Likely a tweet, not a header
                    current = {'tweet': line}
        
        if current and current.get('tweet'):
            tweets.append(current)
        
        cleaned = []
        for t in tweets:
            tweet_text = t.get('tweet', '').strip()
            if tweet_text:
                # Clean up any remaining prefixes
                tweet_text = re.sub(r'^\d+\.\s*', '', tweet_text)
                tweet_text = re.sub(r'^TWEET:\s*', '', tweet_text, flags=re.IGNORECASE)
                cleaned.append({
                    'tweet': tweet_text[:280],
                    'hashtags': t.get('hashtags', '').strip(),
                    'source': t.get('source', '').strip()
                })
        
        return cleaned
