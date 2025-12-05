# Thinking Engine

AI-powered content generation system that analyzes curated research articles and generates blog posts and tweet ideas.

## Overview

The Thinking Engine processes manually curated articles organized by week and generates:
- Fact-based blog posts with inline citations
- Tweet ideas with hashtags and source attribution

Content is generated from your curated sources only—no external ingestion or auto-posting.

## Quick Start

### Local Development

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
echo "OPENAI_API_KEY=your_key_here" > .env

# Run CLI
python -m src.thinking_engine.cli

# Or start API server
python run_api.py
```

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for deploying to Render and setting up CustomGPT.

## Project Structure

```
thinkingengine/
├── src/thinking_engine/    # Core application code
│   ├── api.py              # REST API server
│   ├── cli.py              # Command-line interface
│   ├── document_loaders.py # File parsing
│   ├── llm_orchestrator.py # LLM interaction
│   ├── blog_generator.py   # Blog post generation
│   ├── tweet_generator.py  # Tweet idea generation
│   └── fact_checker.py     # Source validation
├── data/                   # Curated articles (organized by week)
├── output/                 # Generated content
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

## Data Organization

Organize articles in weekly folders:

```
data/
  week-2025-01-15/
    article-001-coindesk-bitcoin.md
    article-002-theblock-defi.md
    report-003-delphi-ethereum.md
```

**Naming**: `{type}-{number}-{source}-{topic}.{ext}`
- Type: `article` or `report`
- Number: Sequential (001, 002, ...)
- Source: Source identifier
- Topic: Brief description

## Usage

### CLI

```bash
# Generate blog post
python -m src.thinking_engine.cli generate-blog week-2025-01-15

# Generate tweet ideas
python -m src.thinking_engine.cli generate-tweets week-2025-01-15 --count 25

# Generate both
python -m src.thinking_engine.cli generate-all week-2025-01-15
```

### API

Start server: `python run_api.py`

Endpoints:
- `GET /api/weeks` - List week folders
- `GET /api/weeks/{week}/documents` - Get documents
- `POST /api/generate/blog` - Generate blog post
- `POST /api/generate/tweets` - Generate tweets
- `POST /api/generate/all` - Generate both

API docs: `http://localhost:8000/docs`

## Configuration

Environment variables (`.env`):
- `OPENAI_API_KEY` - Required
- `OPENAI_MODEL` - Default: `gpt-4o`
- `MAX_CHARS_PER_DOCUMENT` - Default: `12000`
- `MAX_TOTAL_CONTEXT_CHARS` - Default: `50000`

## Output

Generated files in `output/week-YYYY-MM-DD/`:
- `blog-post.md` - Blog post with citations
- `tweet-ideas.json` - Tweet ideas (JSON)
- `tweet-ideas.txt` - Tweet ideas (plain text)

## Testing

```bash
pytest tests/
pytest tests/ -v
```

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment and CustomGPT setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and fixes
- [LARGE_FILES_GUIDE.md](LARGE_FILES_GUIDE.md) - Handling large documents
- [MAINTENANCE.md](MAINTENANCE.md) - Maintenance checklist

## License

MIT
