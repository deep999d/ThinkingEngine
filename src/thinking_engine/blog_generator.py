"""Blog post generation."""

from typing import List, Dict
from pathlib import Path
from .document_loaders import Document
from .llm_orchestrator import LLMOrchestrator
from .fact_checker import FactChecker


class BlogGenerator:
    def __init__(self, llm: LLMOrchestrator):
        self.llm = llm
    
    def generate(self, docs: List[Document], output_path: str) -> Dict:
        if not docs:
            raise ValueError("No documents provided for blog generation")
        
        print("Analyzing documents...")
        summary = self.llm.summarize_documents(docs)
        
        print("Generating blog post...")
        content = self.llm.generate_blog_post(docs, summary)
        
        print("Fact-checking blog post...")
        checker = FactChecker(docs)
        fact_check = checker.check_blog_post(content)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        final_content = content
        if fact_check['has_issues']:
            final_content += "\n\n--- Fact-Check Notes ---\n"
            for issue in fact_check['issues']:
                if issue['type'] == 'invalid_citation':
                    final_content += f"\n⚠️ Invalid citation found: {issue['citation']}\n"
                elif issue['type'] == 'uncited_claims':
                    final_content += f"\n⚠️ Some claims may need citations. Review recommended.\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return {
            'output_file': str(output_file),
            'fact_check': fact_check,
            'summary': summary
        }
