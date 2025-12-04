# AI Content Thinking Engine

An AI agent that analyzes curated text from multiple news and research sources to help craft weekly blog posts and tweet ideas.

## 🚀 Quick Start - Deploy to Render & Use with CustomGPT

**Want to deploy and use this without any local setup?** Follow the complete guide:

👉 **[COMPLETE_DEPLOYMENT_GUIDE.md](COMPLETE_DEPLOYMENT_GUIDE.md)** - Full step-by-step guide (anyone can follow!)

Or for a quick version:
👉 **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - 5 steps, ~15 minutes

**No coding required!** Just follow the guide to:
1. Deploy to Render (free)
2. Set up CustomGPT
3. Start generating content with natural language

---

## Overview

This engine reads manually curated articles from GitHub folders (organized by week) and generates:
- Original, fact-based weekly blog posts with inline citations
- ~25 tweet ideas per week with suggested hashtags/cashtags

**Phase 1 Focus**: Content generation from curated sources only (no ingestion or auto-posting).

## Setup

### Quick Setup (macOS/Linux)

```bash
./setup.sh
```

Then edit `.env` and add your `OPENAI_API_KEY`.

### Manual Setup

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## File Organization

Organize your weekly curated content in the following structure:

```
data/
  week-2024-01-15/
    article-001-coindesk-bitcoin.md
    article-002-theblock-defi.md
    report-003-delphi-ethereum.pdf
    ...
  week-2024-01-22/
    ...
```

### Naming Conventions

- **Weekly folders**: `week-YYYY-MM-DD/` (date of the week)
- **Article files**: `article-XXX-source-topic.ext` or `report-XXX-source-topic.ext`
  - `XXX`: Sequential number (001, 002, etc.)
  - `source`: Short identifier (coindesk, theblock, delphi, fintechtakes)
  - `topic`: Brief topic description
  - `ext`: File extension (.md, .html, .txt, .pdf)

## Usage

### CLI Interface

Run the thinking engine interactively:

```bash
python -m src.thinking_engine.cli
```

Or use the direct command:

```bash
python src/thinking_engine.cli.py
```

### Commands

1. **Generate Blog Post**
   - The CLI will prompt you to select a week folder
   - It will analyze all articles in that folder
   - Generates a blog post draft with citations

2. **Generate Tweet Ideas**
   - Select a week folder
   - Generates ~25 tweet ideas in JSON and plain text formats

3. **Generate Both**
   - Generates both blog post and tweet ideas for a selected week

### REST API (CustomGPT Integration)

The engine also provides a REST API for integration with CustomGPT or other services.

**Start the API server:**
```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

- **Interactive API docs**: Visit `http://localhost:8000/docs` for Swagger UI
- **OpenAPI schema**: Available at `http://localhost:8000/openapi.json`

**Available endpoints:**
- `GET /health` - Health check endpoint
- `GET /api/weeks` - List all week folders
- `GET /api/weeks/{week_folder}/documents` - Get documents in a week folder
- `POST /api/generate/blog` - Generate blog post
- `POST /api/generate/tweets` - Generate tweet ideas
- `POST /api/generate/all` - Generate both blog and tweets

**Deployment:**
- **Complete Guide**: See [COMPLETE_DEPLOYMENT_GUIDE.md](COMPLETE_DEPLOYMENT_GUIDE.md) for full step-by-step deployment and CustomGPT setup (no local setup required!)
- **Local development**: See [CUSTOMGPT_GUIDE.md](CUSTOMGPT_GUIDE.md) for local setup
- **Production (Render)**: See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for deploying to Render with GitHub integration
- **CustomGPT Setup**: See [CUSTOMGPT_SETUP.md](CUSTOMGPT_SETUP.md) for complete step-by-step CustomGPT configuration

## Output

- **Blog Post**: `output/week-YYYY-MM-DD/blog-post.md`
- **Tweet Ideas**: 
  - `output/week-YYYY-MM-DD/tweet-ideas.json`
  - `output/week-YYYY-MM-DD/tweet-ideas.txt`

## Architecture

- `document_loaders.py`: Loads and parses Markdown/HTML/PDF/Plain text files
- `llm_orchestrator.py`: Manages LLM interactions with source-aware prompts
- `blog_generator.py`: Generates blog posts with citations
- `tweet_generator.py`: Generates tweet ideas
- `fact_checker.py`: Validates claims against sources
- `cli.py`: Command-line interface
- `api.py`: REST API server for CustomGPT integration

## Testing

Run tests with sample corpus:

```bash
# Install test dependencies (already in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run smoke tests only
pytest tests/test_smoke.py
```

## Maintenance Checklist

- [ ] Weekly: Add curated articles to `data/week-YYYY-MM-DD/`
- [ ] Weekly: Run CLI to generate content
- [ ] Review generated content for accuracy
- [ ] Update prompts if tone/style needs adjustment
- [ ] Monitor API usage and costs

## Handling Large Files

The engine automatically handles large documents by truncating them intelligently. See [LARGE_FILES_GUIDE.md](LARGE_FILES_GUIDE.md) for details on:
- How truncation works
- Configuring limits in `.env`
- Best practices for large documents
- Cost considerations

Quick config in `.env`:
```bash
MAX_CHARS_PER_DOCUMENT=12000  # Per document limit
MAX_TOTAL_CONTEXT_CHARS=50000  # Total context limit
```

## Notes

- Content is generated only when you interact with the CLI
- All claims are linked to source documents
- Unsupported claims are flagged for review
- No vector store in Phase 1 - uses direct document analysis
- Large files are automatically truncated to fit token limits

