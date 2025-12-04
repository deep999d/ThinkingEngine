# CustomGPT Quick Start

## 1. Start the API Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python run_api.py
```

Server runs on: `http://localhost:8000`

## 2. Get Public URL (for remote access)

**Option A: Using ngrok (for testing)**
```bash
ngrok http 8000
# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

**Option B: Deploy to cloud**
- Deploy to Heroku, Railway, Render, or similar
- Get your production URL

## 3. Configure CustomGPT

### In ChatGPT Custom GPT Builder:

1. **Go to Actions** → **Create new action**

2. **Import OpenAPI Schema:**
   - URL: `{your_url}/openapi.json`
   - Or manually add endpoints (see below)

3. **Add Instructions:**
   ```
   You are a content generation assistant. When users ask to generate content:
   1. List available week folders using GET /api/weeks
   2. Use the specified week folder or ask which one to use
   3. Generate content using POST /api/generate/blog, /api/generate/tweets, or /api/generate/all
   4. Always set return_content=true to get full content
   5. Present results clearly formatted
   ```

## 4. Test It

Try these prompts in your CustomGPT:
- "List all week folders"
- "Generate a blog post for week-2025-01-15"
- "Create 30 tweet ideas for the latest week"

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/weeks` | GET | List week folders |
| `/api/weeks/{week}/documents` | GET | Get documents in a week |
| `/api/generate/blog` | POST | Generate blog post |
| `/api/generate/tweets` | POST | Generate tweets |
| `/api/generate/all` | POST | Generate both |

## Example Request

```json
POST /api/generate/blog
{
  "week_folder": "week-2025-01-15",
  "return_content": true
}
```

## Troubleshooting

- **Can't connect?** Check server is running and URL is correct
- **404 errors?** Verify week folder exists in `data/` directory
- **500 errors?** Check `OPENAI_API_KEY` is set in `.env`

For detailed guide, see [CUSTOMGPT_GUIDE.md](CUSTOMGPT_GUIDE.md)

