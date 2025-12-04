# Maintenance Checklist

## Weekly Tasks

### 1. Curate Articles
- [ ] Review sources (CoinDesk, The Block, Delphi Digital, Fintech Takes)
- [ ] Select relevant articles and reports
- [ ] Download or copy content to appropriate format
- [ ] Save to `data/week-YYYY-MM-DD/` folder following naming conventions

### 2. Generate Content
- [ ] Run CLI: `python -m src.thinking_engine.cli generate-all`
- [ ] Select the week folder when prompted
- [ ] Review generated blog post in `output/week-YYYY-MM-DD/blog-post.md`
- [ ] Review tweet ideas in `output/week-YYYY-MM-DD/tweet-ideas.txt`
- [ ] Check fact-check notes for any flagged issues

### 3. Review and Edit
- [ ] Verify all citations are accurate
- [ ] Check for any unsupported claims
- [ ] Edit blog post for tone and style
- [ ] Select and refine tweet ideas
- [ ] Add any missing context or insights

## Monthly Tasks

- [ ] Review API usage and costs
- [ ] Check for prompt improvements based on output quality
- [ ] Update document loaders if new sources are added
- [ ] Review and clean up old output files if needed

## Troubleshooting

### No documents found
- Check that week folder exists in `data/` directory
- Verify file naming follows convention: `article-XXX-source-topic.ext`
- Ensure files are readable (check permissions)

### API errors
- Verify `OPENAI_API_KEY` is set in `.env` file
- Check API quota and billing
- Try reducing document size if hitting token limits

### Poor quality output
- Review source documents for clarity and completeness
- Adjust temperature in `.env` if output is too creative or too conservative
- Consider splitting very large documents into smaller pieces

### Fact-check issues
- Review flagged citations and verify they match document titles
- Check for claims that need additional source attribution
- Manually verify any statistics or specific numbers

## Configuration Updates

### Adjusting Model Settings
Edit `.env`:
```
OPENAI_MODEL=gpt-4o  # or gpt-4o-mini, gpt-3.5-turbo for faster/cheaper
OPENAI_TEMPERATURE=0.3  # Lower = more deterministic, Higher = more creative
```

### Adding New Sources
1. Update `document_loaders.py` `_extract_source_from_filename()` method
2. Add source identifier to filename pattern matching
3. Test with sample documents

## Backup Recommendations

- Keep weekly folders in version control (Git)
- Archive old output files periodically
- Backup `.env` file securely (never commit to Git)

