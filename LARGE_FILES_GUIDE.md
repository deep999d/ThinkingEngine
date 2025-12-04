# Handling Large Files Guide

The Thinking Engine is designed to handle large documents efficiently. Here's how it works and how to configure it.

## How Large Files Are Handled

### Automatic Truncation

The engine automatically handles large files to stay within token limits:

1. **Per-Document Limit**: Each document is limited to 12,000 characters by default
   - If a document exceeds this, it keeps the **beginning and end**, removing the middle
   - This preserves key information (introductions and conclusions)

2. **Total Context Limit**: All documents combined are limited to 50,000 characters
   - If you have many documents, some may be excluded to stay within limits
   - The engine will warn you which documents were truncated or excluded

3. **Smart Truncation**: Instead of just cutting off the end, the engine:
   - Keeps the first half of the limit
   - Keeps the last half of the limit  
   - Removes the middle section
   - This preserves introductions, conclusions, and key takeaways

## Configuration

You can adjust these limits in your `.env` file:

```bash
# Maximum characters per document (default: 12000)
MAX_CHARS_PER_DOCUMENT=15000

# Maximum total characters for all documents combined (default: 50000)
MAX_TOTAL_CONTEXT_CHARS=60000
```

### Recommended Settings

**For Small Documents (< 5KB each):**
```bash
MAX_CHARS_PER_DOCUMENT=20000
MAX_TOTAL_CONTEXT_CHARS=80000
```

**For Medium Documents (5-20KB each):**
```bash
MAX_CHARS_PER_DOCUMENT=12000  # Default
MAX_TOTAL_CONTEXT_CHARS=50000  # Default
```

**For Large Documents (> 20KB each):**
```bash
MAX_CHARS_PER_DOCUMENT=8000
MAX_TOTAL_CONTEXT_CHARS=40000
```

## Best Practices

### 1. Pre-process Large Files

Before adding files to your weekly folder:

- **Extract key sections**: Copy only the relevant parts of long reports
- **Remove boilerplate**: Delete headers, footers, disclaimers
- **Summarize**: For very long documents, create a summary version

### 2. Split Large Documents

Instead of one huge file, split into focused documents:

```
❌ report-001-delphi-full-analysis.pdf (50 pages)

✅ report-001-delphi-executive-summary.md
✅ report-002-delphi-market-analysis.md
✅ report-003-delphi-technical-details.md
```

### 3. Use Markdown Format

Markdown files are processed more efficiently than PDFs:

- PDFs require text extraction (can be slow/lossy)
- Markdown preserves structure better
- Easier to edit and truncate manually if needed

### 4. Monitor Warnings

The engine will warn you when:
- Files are larger than 5MB
- Documents are truncated
- Documents are excluded due to context limits

Pay attention to these warnings to ensure important content isn't lost.

## Example Workflow

### Scenario: You have 3 large PDF reports (each 30+ pages)

**Option 1: Pre-process (Recommended)**
1. Extract executive summaries from each PDF
2. Save as: `report-001-delphi-summary.md`, etc.
3. Add to weekly folder
4. Run generation

**Option 2: Use Default Settings**
1. Add full PDFs to weekly folder
2. Engine will automatically truncate each to ~12K chars
3. Review warnings to see what was truncated
4. If important content is missing, use Option 1

**Option 3: Increase Limits**
1. Set in `.env`: `MAX_CHARS_PER_DOCUMENT=20000`
2. Set in `.env`: `MAX_TOTAL_CONTEXT_CHARS=80000`
3. Note: This increases API costs and may hit token limits

## Token Limits by Model

Different models have different context windows:

- **GPT-4o**: ~128K tokens (~500K characters)
- **GPT-4o-mini**: ~128K tokens (~500K characters)
- **GPT-3.5-turbo**: ~16K tokens (~64K characters)

The default settings (50K total chars) work well for all models and leave room for:
- System prompts
- Generated output
- Response overhead

## Troubleshooting

### "Documents were truncated" warning

**What it means**: Some documents were too long and had content removed.

**What to do**:
1. Check which documents were truncated (shown in warning)
2. Review the generated content - is important info missing?
3. If yes, pre-process those documents to extract key sections
4. Re-run generation

### "Stopping at document X" warning

**What it means**: Too many documents - some were excluded entirely.

**What to do**:
1. Reduce number of documents (aim for 3-10 per week)
2. Or increase `MAX_TOTAL_CONTEXT_CHARS` in `.env`
3. Or split into multiple week folders

### Very slow processing

**Possible causes**:
- Very large PDF files (slow to extract text)
- Many documents (processing each one)
- Network issues (API calls)

**Solutions**:
- Convert PDFs to Markdown first
- Reduce number of documents
- Use smaller model (gpt-4o-mini) for faster processing

## Cost Considerations

Larger context = higher costs:

- **Small context** (~20K chars): ~$0.01-0.02 per generation
- **Medium context** (~50K chars): ~$0.02-0.05 per generation  
- **Large context** (~100K chars): ~$0.05-0.10 per generation

Using the default settings keeps costs reasonable while handling most use cases.

