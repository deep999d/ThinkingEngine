"""Tests for fact checker."""

import pytest
from src.thinking_engine.document_loaders import Document
from src.thinking_engine.fact_checker import FactChecker


def test_extract_citations():
    """Test citation extraction from content."""
    doc1 = Document("test1.md", "Bitcoin reached $50k", "coindesk", "Bitcoin News")
    checker = FactChecker([doc1])
    
    content = "Bitcoin is up [Source: Bitcoin News]. Ethereum also rose [Source: Ethereum Report]."
    citations = checker._extract_citations(content)
    
    assert len(citations) == 2
    assert "Bitcoin News" in citations
    assert "Ethereum Report" in citations


def test_citation_exists():
    """Test citation validation."""
    doc1 = Document("test1.md", "Content", "coindesk", "Bitcoin News")
    doc2 = Document("test2.md", "Content", "theblock", "DeFi Report")
    
    checker = FactChecker([doc1, doc2])
    
    assert checker._citation_exists("Bitcoin News")
    assert checker._citation_exists("DeFi Report")
    assert not checker._citation_exists("Non-existent Document")


def test_check_blog_post():
    """Test blog post fact-checking."""
    doc1 = Document("test1.md", "Bitcoin reached $50,000 today", "coindesk", "Bitcoin News")
    checker = FactChecker([doc1])
    
    # Valid blog post with citation
    blog_content = "Bitcoin surged to new heights [Source: Bitcoin News]. The price reached $50,000."
    result = checker.check_blog_post(blog_content)
    
    assert result['citation_count'] == 1
    # Should not have major issues if citation is valid
    assert result['citation_count'] > 0


def test_check_tweet_ideas():
    """Test tweet ideas fact-checking."""
    doc1 = Document("test1.md", "Bitcoin reached $50,000", "coindesk", "Bitcoin News")
    checker = FactChecker([doc1])
    
    tweets = [
        {"tweet": "Bitcoin hit $50,000 today!", "hashtags": "#Bitcoin $BTC", "source": "Bitcoin News"},
        {"tweet": "Great day for crypto", "hashtags": "#crypto", "source": ""},
    ]
    
    result = checker.check_tweet_ideas(tweets)
    # Should not have critical issues for these tweets
    assert isinstance(result, dict)
    assert 'has_issues' in result

