"""Document loaders for various file formats."""

import re
from pathlib import Path
from typing import List, Optional
import markdown
from bs4 import BeautifulSoup
import PyPDF2


class Document:
    def __init__(self, file_path: str, content: str, source: str, title: Optional[str] = None):
        self.file_path = file_path
        self.content = content
        self.source = source
        self.title = title or self._extract_title(file_path)
        self.file_type = Path(file_path).suffix.lower()
    
    def _extract_title(self, file_path: str) -> str:
        filename = Path(file_path).stem
        title = re.sub(r'^(article|report)-\d+-', '', filename)
        title = title.replace('-', ' ').replace('_', ' ')
        return title.title()
    
    def __repr__(self):
        return f"Document({self.source}, {self.title[:50]}...)"


class DocumentLoader:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
    
    def load_week_folder(self, week_folder: str) -> List[Document]:
        week_path = self.base_path / week_folder
        
        if not week_path.exists():
            raise ValueError(f"Week folder not found: {week_path}")
        
        docs = []
        large_files = []
        
        for file_path in sorted(week_path.iterdir()):
            if not file_path.is_file():
                continue
                
            try:
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                if file_size_mb > 5:
                    large_files.append((file_path.name, file_size_mb))
                
                doc = self.load_document(str(file_path))
                if doc:
                    content_mb = len(doc.content) / (1024 * 1024)
                    if content_mb > 2:
                        print(f"⚠️  Large document: {doc.title} ({content_mb:.1f} MB text)")
                    docs.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load {file_path}: {e}")
        
        if large_files:
            print(f"\n⚠️  Found {len(large_files)} large file(s) (>5MB):")
            for name, size in large_files[:5]:
                print(f"   - {name}: {size:.1f} MB")
            if len(large_files) > 5:
                print(f"   ... and {len(large_files) - 5} more")
            print("   Large files will be truncated to fit token limits.\n")
        
        return docs
    
    def load_document(self, file_path: str) -> Optional[Document]:
        path = Path(file_path)
        if not path.exists():
            return None
        
        ext = path.suffix.lower()
        source = self._get_source(path.name)
        
        loaders = {
            '.md': self._load_markdown,
            '.html': self._load_html,
            '.pdf': self._load_pdf,
            '.txt': self._load_text,
        }
        
        loader = loaders.get(ext)
        if not loader:
            print(f"Unsupported file type: {ext}")
            return None
        
        content = loader(file_path)
        if not content or not content.strip():
            return None
        
        return Document(file_path, content, source)
    
    def _load_markdown(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    
    def _load_html(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)
    
    def _load_pdf(self, file_path: str) -> str:
        parts = []
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return '\n\n'.join(parts)
    
    def _load_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_source(self, filename: str) -> str:
        match = re.search(r'-(coindesk|theblock|delphi|fintechtakes|block|digital|takes)-', filename.lower())
        if match:
            return match.group(1)
        stem = Path(filename).stem
        return stem.split('-')[0] if '-' in stem else "unknown"
    
    def list_week_folders(self) -> List[str]:
        if not self.base_path.exists():
            return []
        
        folders = [
            item.name for item in self.base_path.iterdir()
            if item.is_dir() and item.name.startswith('week-')
        ]
        return sorted(folders, reverse=True)
