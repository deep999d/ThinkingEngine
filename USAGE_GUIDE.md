# Usage Guide

## Quick Start

1. **Set up your environment** (one-time)
   ```bash
   ./setup.sh
   # Edit .env and add OPENAI_API_KEY
   ```

2. **Add your curated articles**
   - Create a folder: `data/week-2024-01-15/`
   - Add articles following naming convention: `article-001-coindesk-topic.md`
   - See `data/README.md` for details

3. **Generate content**
   ```bash
   python -m src.thinking_engine.cli generate-all
   ```

4. **Review output**
   - Blog post: `output/week-2024-01-15/blog-post.md`
   - Tweet ideas: `output/week-2024-01-15/tweet-ideas.txt`

## CLI Commands

### Generate Blog Post Only

```bash
python -m src.thinking_engine.cli generate-blog
```

You'll be prompted to select a week folder, or you can specify it:

```bash
python -m src.thinking_engine.cli generate-blog week-2024-01-15
```

### Generate Tweet Ideas Only

```bash
python -m src.thinking_engine.cli generate-tweets
```

Generate a specific number of tweets:

```bash
python -m src.thinking_engine.cli generate-tweets --count 30
```

### Generate Both

```bash
python -m src.thinking_engine.cli generate-all
```

### List Available Weeks

```bash
python -m src.thinking_engine.cli list-weeks
```

## Workflow Example

### Weekly Routine

1. **Monday**: Curate articles from your sources
   - Save to `data/week-2024-01-15/`
   - Use consistent naming: `article-001-coindesk-bitcoin.md`

2. **Tuesday**: Generate content
   ```bash
   python -m src.thinking_engine.cli generate-all week-2024-01-15
   ```

3. **Wednesday**: Review and edit
   - Open `output/week-2024-01-15/blog-post.md`
   - Check fact-check notes
   - Edit for tone and style
   - Select best tweets from `tweet-ideas.txt`

4. **Thursday-Friday**: Publish
   - Post blog to your platform
   - Schedule selected tweets

## File Naming Best Practices

### Good Examples
- `article-001-coindesk-bitcoin-etf.md`
- `article-002-theblock-defi-tvl.md`
- `report-003-delphi-ethereum-upgrade.md`
- `article-004-fintechtakes-regulation.md`

### What to Avoid
- `bitcoin-news.md` (missing structure)
- `article1.md` (missing source)
- `coindesk article.md` (spaces, missing number)

## Tips for Better Output

### 1. Quality Sources
- Use complete articles, not just snippets
- Include context and background information
- Prefer longer, detailed reports over short news items

### 2. Document Organization
- Keep related topics together in the same week
- Don't mix unrelated topics (e.g., Bitcoin and DeFi regulation in same week)
- Aim for 3-10 articles per week for best results

### 3. Content Format
- **Markdown** is preferred (best parsing)
- Include source attribution in the document itself
- Keep formatting clean and readable

### 4. Review Process
- Always check fact-check notes
- Verify citations match your documents
- Edit for your unique voice and perspective
- Add personal insights that the AI might miss

## Troubleshooting

### "No week folders found"
- Create a folder in `data/` with format `week-YYYY-MM-DD/`
- Ensure folder name starts with `week-`

### "No documents found"
- Check file naming follows convention
- Verify files are readable (not corrupted)
- Check file extensions are supported (.md, .html, .txt, .pdf)

### "OPENAI_API_KEY not found"
- Check `.env` file exists
- Verify key is set: `OPENAI_API_KEY=sk-...`
- Restart terminal after creating `.env`

### Poor quality output
- Try increasing number of source documents
- Check documents are complete and well-formatted
- Adjust temperature in `.env` (lower = more conservative)

### API errors
- Check API key is valid
- Verify you have API credits
- Check rate limits haven't been exceeded

## Advanced Usage

### Custom Model Configuration

Edit `.env`:
```bash
OPENAI_MODEL=gpt-4o  # or gpt-4o-mini, gpt-3.5-turbo
OPENAI_TEMPERATURE=0.3  # 0.0-1.0, lower = more deterministic
```

### Programmatic Usage

You can also use the engine programmatically:

```python
from src.thinking_engine.document_loaders import DocumentLoader
from src.thinking_engine.llm_orchestrator import LLMOrchestrator
from src.thinking_engine.blog_generator import BlogGenerator

# Load documents
loader = DocumentLoader()
documents = loader.load_week_folder("week-2024-01-15")

# Generate blog
llm = LLMOrchestrator()
blog_gen = BlogGenerator(llm)
result = blog_gen.generate(documents, "output/blog.md")
```

## Next Steps

- Review generated content carefully
- Customize prompts in `llm_orchestrator.py` for your style
- Build your weekly routine
- Consider Phase 2 features (auto-ingestion, vector store)

