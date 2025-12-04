"""Tweet idea generation."""

import json
from typing import List, Dict
from pathlib import Path
from .document_loaders import Document
from .llm_orchestrator import LLMOrchestrator
from .fact_checker import FactChecker


class TweetGenerator:
    def __init__(self, llm: LLMOrchestrator, count: int = 25):
        self.llm = llm
        self.count = count
    
    def generate(self, docs: List[Document], output_dir: str) -> Dict:
        if not docs:
            raise ValueError("No documents provided for tweet generation")
        
        print("Analyzing documents...")
        summary = self.llm.summarize_documents(docs)
        
        print(f"Generating {self.count} tweet ideas...")
        tweets = self.llm.generate_tweet_ideas(docs, summary, self.count)
        
        print("Fact-checking tweet ideas...")
        checker = FactChecker(docs)
        fact_check = checker.check_tweet_ideas(tweets)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        json_file = output_path / "tweet-ideas.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'tweets': tweets,
                'fact_check': fact_check,
                'count': len(tweets)
            }, f, indent=2, ensure_ascii=False)
        
        txt_file = output_path / "tweet-ideas.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Tweet Ideas ({len(tweets)} total)\n")
            f.write("=" * 50 + "\n\n")
            
            for i, tweet in enumerate(tweets, 1):
                f.write(f"{i}. {tweet['tweet']}\n")
                if tweet.get('hashtags'):
                    f.write(f"   Tags: {tweet['hashtags']}\n")
                if tweet.get('source'):
                    f.write(f"   Source: {tweet['source']}\n")
                f.write("\n")
            
            if fact_check['has_issues']:
                f.write("\n--- Fact-Check Notes ---\n")
                for issue in fact_check['issues']:
                    if issue['type'] == 'tweets_missing_sources':
                        f.write(f"\n⚠️ Some tweets may need source attribution.\n")
        
        return {
            'json_file': str(json_file),
            'txt_file': str(txt_file),
            'tweet_count': len(tweets),
            'fact_check': fact_check
        }
