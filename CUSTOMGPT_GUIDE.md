# CustomGPT Integration Guide

This guide explains how to use the Thinking Engine API with CustomGPT (OpenAI's Custom GPTs feature).

## Overview

The Thinking Engine API provides REST endpoints that can be integrated with CustomGPT, allowing you to generate blog posts and tweet ideas through natural language prompts in ChatGPT.

## Quick Start

### 1. Start the API Server

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the API server
python run_api.py
```

The server will start on `http://localhost:8000`

### 2. Test the API

Visit `http://localhost:8000/docs` in your browser to see the interactive API documentation (Swagger UI).

You can test endpoints directly from the browser interface.

### 3. For Production/Remote Access

If you want to use this with CustomGPT from a remote location, you'll need to:

1. **Deploy the API** to a cloud service (e.g., Heroku, Railway, Render, AWS, etc.)
2. **Or use a tunneling service** like ngrok for local development:
   ```bash
   # Install ngrok: https://ngrok.com/
   ngrok http 8000
   ```
   This will give you a public URL like `https://abc123.ngrok.io`

## CustomGPT Configuration

### Option 1: Using Actions (Recommended)

1. Go to ChatGPT → Create a Custom GPT
2. In the "Actions" section, add a new action
3. Use the OpenAPI schema from: `http://localhost:8000/openapi.json`
4. Or manually configure the following endpoints:

#### Available Actions:

**List Week Folders**
- Method: GET
- URL: `{base_url}/api/weeks`
- Description: Get all available week folders

**Get Week Documents**
- Method: GET
- URL: `{base_url}/api/weeks/{week_folder}/documents`
- Description: Get documents in a specific week folder

**Generate Blog Post**
- Method: POST
- URL: `{base_url}/api/generate/blog`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "return_content": true
  }
  ```

**Generate Tweet Ideas**
- Method: POST
- URL: `{base_url}/api/generate/tweets`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "count": 25,
    "return_content": true
  }
  ```

**Generate Both**
- Method: POST
- URL: `{base_url}/api/generate/all`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "tweet_count": 25,
    "return_content": true
  }
  ```

### Option 2: Using Instructions

Add these instructions to your CustomGPT:

```
You are a content generation assistant that uses the Thinking Engine API.

When the user asks to generate content:
1. First, list available week folders using GET /api/weeks
2. If the user specifies a week folder, use it. Otherwise, ask which one to use.
3. Generate the requested content (blog post, tweets, or both) using the appropriate endpoint.
4. Present the results in a clear, formatted way.

Available endpoints:
- GET /api/weeks - List week folders
- GET /api/weeks/{week_folder}/documents - Get documents in a week folder
- POST /api/generate/blog - Generate blog post
- POST /api/generate/tweets - Generate tweet ideas
- POST /api/generate/all - Generate both blog and tweets

Always set return_content=true to get the full content in the response.
```

## Example Prompts for CustomGPT

Once configured, you can use natural language prompts like:

- "List all available week folders"
- "Generate a blog post for week-2025-01-15"
- "Create 30 tweet ideas for the latest week"
- "Generate both blog post and tweets for week-2025-01-15"
- "What documents are in week-2025-01-15?"

## API Endpoints Reference

### GET `/`
Root endpoint with API information.

### GET `/api/weeks`
List all available week folders.

**Response:**
```json
{
  "week_folders": ["week-2025-01-15", "week-2025-01-22"],
  "count": 2
}
```

### GET `/api/weeks/{week_folder}/documents`
Get documents in a specific week folder.

**Response:**
```json
{
  "week_folder": "week-2025-01-15",
  "documents": [
    {
      "title": "Coindesk Bitcoin",
      "source": "coindesk",
      "file_path": "data/week-2025-01-15/article-001-coindesk-bitcoin.md",
      "file_type": ".md"
    }
  ],
  "count": 1
}
```

### POST `/api/generate/blog`
Generate a blog post.

**Request:**
```json
{
  "week_folder": "week-2025-01-15",
  "return_content": true
}
```

**Response:**
```json
{
  "success": true,
  "week_folder": "week-2025-01-15",
  "output_file": "output/week-2025-01-15/blog-post.md",
  "citation_count": 5,
  "has_fact_check_issues": false,
  "fact_check_issues": [],
  "content": "# Blog Post Content...",
  "message": "Blog post generated successfully"
}
```

### POST `/api/generate/tweets`
Generate tweet ideas.

**Request:**
```json
{
  "week_folder": "week-2025-01-15",
  "count": 25,
  "return_content": true
}
```

**Response:**
```json
{
  "success": true,
  "week_folder": "week-2025-01-15",
  "json_file": "output/week-2025-01-15/tweet-ideas.json",
  "txt_file": "output/week-2025-01-15/tweet-ideas.txt",
  "tweet_count": 25,
  "has_fact_check_issues": false,
  "fact_check_issues": [],
  "tweets": [
    {
      "tweet": "Example tweet text...",
      "hashtags": "#crypto #bitcoin",
      "source": "coindesk"
    }
  ],
  "message": "Generated 25 tweet ideas successfully"
}
```

### POST `/api/generate/all`
Generate both blog post and tweet ideas.

**Request:**
```json
{
  "week_folder": "week-2025-01-15",
  "tweet_count": 25,
  "return_content": true
}
```

## Authentication

Currently, the API doesn't require authentication. For production use, you should:

1. Add API key authentication
2. Use HTTPS
3. Implement rate limiting
4. Add request validation

## Troubleshooting

### API Server Won't Start
- Check that port 8000 is not in use
- Verify `OPENAI_API_KEY` is set in `.env`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### CustomGPT Can't Connect
- Verify the API server is running and accessible
- Check the base URL is correct (include `http://` or `https://`)
- For local development, use ngrok or similar tunneling service
- Check CORS settings if accessing from a browser

### Generation Errors
- Verify week folder exists in `data/` directory
- Check that week folder contains documents
- Ensure `OPENAI_API_KEY` is valid and has credits
- Check API logs for detailed error messages

## Security Considerations

For production deployment:

1. **Add Authentication**: Implement API key or OAuth authentication
2. **Use HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Input Validation**: Validate all inputs server-side
5. **Error Handling**: Don't expose sensitive information in error messages
6. **CORS**: Restrict CORS to specific origins instead of `*`

## Next Steps

- Deploy to a cloud service for 24/7 availability
- Add authentication and rate limiting
- Set up monitoring and logging
- Create a custom GPT with optimized prompts for your use case

