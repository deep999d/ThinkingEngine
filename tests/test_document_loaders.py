"""Tests for document loaders."""

import pytest
from pathlib import Path
from src.thinking_engine.document_loaders import DocumentLoader, Document


def test_document_loader_initialization():
    """Test DocumentLoader can be initialized."""
    loader = DocumentLoader(base_path="data")
    assert loader.base_path == Path("data")


def test_load_markdown_document(tmp_path):
    """Test loading a Markdown document."""
    # Create a test markdown file
    test_file = tmp_path / "test-article.md"
    test_file.write_text("""
# Test Article

This is a test article about Bitcoin.

## Section 1

Bitcoin is a cryptocurrency.
""")
    
    loader = DocumentLoader(base_path=str(tmp_path))
    doc = loader.load_document(str(test_file))
    
    assert doc is not None
    assert "Bitcoin" in doc.content
    assert doc.file_type == ".md"
    assert doc.source in doc.file_path


def test_load_text_document(tmp_path):
    """Test loading a plain text document."""
    test_file = tmp_path / "article-001-coindesk-test.txt"
    test_file.write_text("This is a plain text article about Ethereum and DeFi.")
    
    loader = DocumentLoader(base_path=str(tmp_path))
    doc = loader.load_document(str(test_file))
    
    assert doc is not None
    assert "Ethereum" in doc.content
    assert doc.file_type == ".txt"


def test_extract_source_from_filename():
    """Test source extraction from filename."""
    loader = DocumentLoader()
    
    assert "coindesk" in loader._extract_source_from_filename("article-001-coindesk-bitcoin.md").lower()
    assert "theblock" in loader._extract_source_from_filename("article-002-theblock-defi.md").lower()
    assert "delphi" in loader._extract_source_from_filename("report-003-delphi-ethereum.md").lower()


def test_load_week_folder(tmp_path):
    """Test loading all documents from a week folder."""
    week_folder = tmp_path / "week-2024-01-15"
    week_folder.mkdir()
    
    # Create test files
    (week_folder / "article-001-coindesk-test.md").write_text("# Test 1")
    (week_folder / "article-002-theblock-test.txt").write_text("Test 2")
    
    loader = DocumentLoader(base_path=str(tmp_path))
    documents = loader.load_week_folder("week-2024-01-15")
    
    assert len(documents) == 2
    assert all(isinstance(doc, Document) for doc in documents)


def test_list_week_folders(tmp_path):
    """Test listing available week folders."""
    # Create test week folders
    (tmp_path / "week-2024-01-15").mkdir()
    (tmp_path / "week-2024-01-22").mkdir()
    (tmp_path / "other-folder").mkdir()  # Should be ignored
    
    loader = DocumentLoader(base_path=str(tmp_path))
    folders = loader.list_week_folders()
    
    assert len(folders) == 2
    assert "week-2024-01-15" in folders
    assert "week-2024-01-22" in folders
    assert "other-folder" not in folders

