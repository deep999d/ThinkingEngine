"""Smoke tests with sample corpus."""

import pytest
from pathlib import Path
from src.thinking_engine.document_loaders import DocumentLoader
from src.thinking_engine.fact_checker import FactChecker


def test_smoke_load_sample_corpus():
    """Smoke test: Load sample documents from example week folder."""
    loader = DocumentLoader(base_path="data")
    
    # Check if example week folder exists
    week_folder = "week-2024-01-15"
    week_path = Path("data") / week_folder
    
    if not week_path.exists():
        pytest.skip(f"Sample corpus not found at {week_path}")
    
    # Load documents
    documents = loader.load_week_folder(week_folder)
    
    assert len(documents) > 0, "Should have at least one document"
    
    # Verify document structure
    for doc in documents:
        assert doc.content, "Document should have content"
        assert doc.source, "Document should have source"
        assert doc.title, "Document should have title"
        assert doc.file_path, "Document should have file path"


def test_smoke_fact_checker_with_sample():
    """Smoke test: Fact checker works with sample documents."""
    loader = DocumentLoader(base_path="data")
    week_folder = "week-2024-01-15"
    week_path = Path("data") / week_folder
    
    if not week_path.exists():
        pytest.skip(f"Sample corpus not found at {week_path}")
    
    documents = loader.load_week_folder(week_folder)
    
    if not documents:
        pytest.skip("No documents to test with")
    
    checker = FactChecker(documents)
    
    # Test with sample content
    test_content = "Bitcoin reached new highs [Source: Bitcoin News]. The market is growing."
    result = checker.check_blog_post(test_content)
    
    assert isinstance(result, dict)
    assert 'has_issues' in result
    assert 'citation_count' in result


def test_smoke_list_week_folders():
    """Smoke test: Can list week folders."""
    loader = DocumentLoader(base_path="data")
    folders = loader.list_week_folders()
    
    # Should at least find the example folder if it exists
    assert isinstance(folders, list)

