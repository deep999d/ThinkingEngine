# Quick Start Guide

## 1. Initial Setup (One-Time)

```bash
# Run setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

## 2. Add Your Articles

Create a week folder and add articles:

```bash
mkdir -p data/week-2024-01-15
# Add files like:
# - article-001-coindesk-bitcoin.md
# - article-002-theblock-defi.md
# - report-003-delphi-ethereum.md
```

## 3. Generate Content

```bash
# Activate venv (if not already active)
source venv/bin/activate

# Generate both blog and tweets
python -m src.thinking_engine.cli generate-all

# Or generate separately:
python -m src.thinking_engine.cli generate-blog
python -m src.thinking_engine.cli generate-tweets
```

## 4. Review Output

- Blog: `output/week-2024-01-15/blog-post.md`
- Tweets: `output/week-2024-01-15/tweet-ideas.txt`

## File Naming Convention

Format: `[type]-[number]-[source]-[topic].[ext]`

Examples:
- `article-001-coindesk-bitcoin.md`
- `article-002-theblock-defi.md`
- `report-003-delphi-ethereum.md`

## Common Commands

```bash
# List available weeks
python -m src.thinking_engine.cli list-weeks

# Generate for specific week
python -m src.thinking_engine.cli generate-all week-2024-01-15

# Generate 30 tweets instead of 25
python -m src.thinking_engine.cli generate-tweets --count 30
```

## Need Help?

- Full docs: `README.md`
- Usage guide: `USAGE_GUIDE.md`
- Maintenance: `MAINTENANCE.md`

