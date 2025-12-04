# Render Deployment Guide

This guide walks you through deploying the Thinking Engine API to Render for use with CustomGPT.

## Prerequisites

1. **GitHub Account** - Your code and data files will be stored in GitHub
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. **OpenAI API Key** - For generating content

## Step 1: Prepare Your Repository

### 1.1 Ensure Data Directory is Tracked

The `data/` directory should be committed to GitHub. Check that it's not in `.gitignore`:

```bash
# Verify data/ is not ignored
git check-ignore data/
# Should return nothing if data/ is tracked
```

If `data/` is ignored, remove it from `.gitignore`:

```bash
# Remove data/ from .gitignore if present
```

### 1.2 Commit Your Code and Data

```bash
# Add all files including data directory
git add .

# Commit
git commit -m "Add Thinking Engine API with data files"

# Push to GitHub
git push origin main
```

**Important**: Make sure your `data/` directory with week folders is committed to the repository.

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Blueprint"

2. **Connect GitHub Repository**
   - Select your repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**
   - In the service settings, go to "Environment"
   - Add the following:
     - `OPENAI_API_KEY`: Your OpenAI API key (mark as "Secret")
     - `OPENAI_MODEL`: `gpt-4o` (optional, defaults to gpt-4o)
     - `MAX_CHARS_PER_DOCUMENT`: `12000` (optional)
     - `MAX_TOTAL_CONTEXT_CHARS`: `50000` (optional)

4. **Deploy**
   - Render will automatically build and deploy
   - Wait for deployment to complete (usually 2-5 minutes)

### Option B: Manual Setup

1. **Create New Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `thinking-engine-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_api.py`
   - **Health Check Path**: `/health`

3. **Set Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: `gpt-4o` (optional)
   - `MAX_CHARS_PER_DOCUMENT`: `12000` (optional)
   - `MAX_TOTAL_CONTEXT_CHARS`: `50000` (optional)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

## Step 3: Get Your API URL

After deployment, Render will provide a URL like:
- `https://thinking-engine-api.onrender.com`

**Note**: On the free tier, services spin down after 15 minutes of inactivity. The first request after spin-down may take 30-60 seconds.

## Step 4: Configure CustomGPT

### 4.1 Get OpenAPI Schema

Visit your deployed API's OpenAPI schema:
```
https://your-app-name.onrender.com/openapi.json
```

### 4.2 Configure CustomGPT Actions

1. **Go to ChatGPT** → Create or edit your Custom GPT
2. **Navigate to Actions** → "Create new action"
3. **Import Schema**:
   - Paste the OpenAPI schema URL: `https://your-app-name.onrender.com/openapi.json`
   - Or manually configure endpoints (see below)

### 4.3 Add Instructions

Add these instructions to your CustomGPT:

```
You are a content generation assistant powered by the Thinking Engine API.

When users request content generation:
1. First, list available week folders using GET /api/weeks
2. If the user specifies a week folder, use it. Otherwise, ask which one to use.
3. Generate content using:
   - POST /api/generate/blog - for blog posts
   - POST /api/generate/tweets - for tweet ideas
   - POST /api/generate/all - for both
4. Always set return_content=true to get full content in response
5. Present results in a clear, formatted way with proper markdown

The API is deployed at: https://your-app-name.onrender.com
```

### 4.4 Manual Endpoint Configuration (Alternative)

If automatic schema import doesn't work, manually add these actions:

**List Week Folders**
- Method: `GET`
- URL: `https://your-app-name.onrender.com/api/weeks`

**Get Week Documents**
- Method: `GET`
- URL: `https://your-app-name.onrender.com/api/weeks/{week_folder}/documents`

**Generate Blog Post**
- Method: `POST`
- URL: `https://your-app-name.onrender.com/api/generate/blog`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "return_content": true
  }
  ```

**Generate Tweets**
- Method: `POST`
- URL: `https://your-app-name.onrender.com/api/generate/tweets`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "count": 25,
    "return_content": true
  }
  ```

**Generate All**
- Method: `POST`
- URL: `https://your-app-name.onrender.com/api/generate/all`
- Body:
  ```json
  {
    "week_folder": "week-2025-01-15",
    "tweet_count": 25,
    "return_content": true
  }
  ```

## Step 5: Test Your Deployment

### 5.1 Test API Directly

Visit your API docs:
```
https://your-app-name.onrender.com/docs
```

Test the health endpoint:
```
https://your-app-name.onrender.com/health
```

### 5.2 Test in CustomGPT

Try these prompts:
- "List all available week folders"
- "Generate a blog post for week-2025-01-15"
- "Create 30 tweet ideas for the latest week"

## Updating Data Files

Since data files are stored in GitHub:

1. **Add new week folders** to `data/week-YYYY-MM-DD/` locally
2. **Commit and push** to GitHub:
   ```bash
   git add data/week-YYYY-MM-DD/
   git commit -m "Add week YYYY-MM-DD articles"
   git push origin main
   ```
3. **Render will auto-deploy** (if auto-deploy is enabled)
4. **Or manually redeploy** from Render dashboard

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model to use |
| `MAX_CHARS_PER_DOCUMENT` | No | `12000` | Max chars per document |
| `MAX_TOTAL_CONTEXT_CHARS` | No | `50000` | Max total context chars |
| `PORT` | No | `8000` | Server port (set by Render) |
| `DEBUG` | No | `false` | Enable debug mode |

## Troubleshooting

### Deployment Fails

1. **Check build logs** in Render dashboard
2. **Verify requirements.txt** is correct
3. **Check Python version** (Render uses Python 3.11 by default)
4. **Verify all dependencies** are in requirements.txt

### API Returns 500 Errors

1. **Check environment variables** are set correctly
2. **Verify OPENAI_API_KEY** is valid
3. **Check Render logs** for error messages
4. **Test locally** first to isolate issues

### CustomGPT Can't Connect

1. **Verify API is accessible**: Visit `https://your-app-name.onrender.com/health`
2. **Check CORS settings**: API allows all origins (`*`)
3. **Verify URL** in CustomGPT actions is correct
4. **Check Render service** is not sleeping (free tier spins down)

### Service is Slow to Respond

- **First request after spin-down**: Free tier services sleep after 15 min inactivity
- **Cold start**: First request may take 30-60 seconds
- **Upgrade to paid tier** for always-on service

### Data Files Not Found

1. **Verify data/ directory** is committed to GitHub
2. **Check file paths** in error messages
3. **Verify week folder names** match exactly (case-sensitive)

## Monitoring

### Health Check

Monitor your service health:
```
GET https://your-app-name.onrender.com/health
```

Returns:
```json
{
  "status": "healthy",
  "data_directory_exists": true,
  "api_key_configured": true,
  "version": "0.1.0"
}
```

### Logs

View logs in Render dashboard:
- Go to your service
- Click "Logs" tab
- Monitor for errors and API usage

## Cost Considerations

### Render Free Tier
- **750 hours/month** free
- **Services sleep** after 15 min inactivity
- **512 MB RAM**
- **Sufficient for light usage**

### OpenAI API Costs
- **GPT-4o**: ~$2.50-5.00 per 1M input tokens
- **Typical blog post**: ~50K-100K tokens
- **Monitor usage** in OpenAI dashboard

## Security Best Practices

1. **Never commit** `.env` file or API keys
2. **Use Render secrets** for sensitive environment variables
3. **Consider adding authentication** for production use
4. **Monitor API usage** to detect abuse
5. **Set up rate limiting** if needed

## Next Steps

- Set up monitoring and alerts
- Add authentication if needed
- Configure custom domain (Render Pro)
- Set up CI/CD for automated deployments
- Add request logging and analytics

## Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **CustomGPT Docs**: [platform.openai.com/docs/guides/custom-gpts](https://platform.openai.com/docs/guides/custom-gpts)

