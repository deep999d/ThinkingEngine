# Deployment Guide

Step-by-step guide for deploying to Render and configuring CustomGPT.

## Prerequisites

- GitHub account
- Render account ([render.com](https://render.com))
- OpenAI account with API key
- ChatGPT Plus or Enterprise (for CustomGPT)

## Part 1: Deploy to Render

### 1. Prepare Repository

1. Push code to GitHub (include `data/` folder)
2. Verify `render.yaml` and `Procfile` are in root

### 2. Deploy Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Blueprint"
3. Connect GitHub repository
4. Render auto-detects `render.yaml`
5. Click "Apply"

### 3. Configure Environment

In Render dashboard → Your service → Environment:

- `OPENAI_API_KEY` - Your OpenAI API key (mark as Secret)
- `API_BASE_URL` - Your Render URL (e.g., `https://your-app.onrender.com`)
- `OPENAI_MODEL` - Optional, default: `gpt-4o`

### 4. Verify Deployment

1. Wait for deployment (2-5 minutes)
2. Test: `https://your-app.onrender.com/health`
3. Should return: `{"status": "healthy", ...}`

## Part 2: Configure CustomGPT

### 1. Create CustomGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Profile → "My GPTs" → "Create"

### 2. Basic Settings

- **Name**: Thinking Engine
- **Description**: AI content generator for blog posts and tweets

### 3. Configure Actions

1. Go to "Configure" → "Actions"
2. Click "Create new action"
3. **Import schema**: `https://your-app.onrender.com/openapi.json`
4. If import fails, add manually (see below)

**Manual Configuration** (if import doesn't work):

For each endpoint:
- **Authentication**: None
- **Method**: GET or POST
- **URL**: `https://your-app.onrender.com/api/...`
- **Body**: JSON for POST requests

### 4. Add Instructions

```
You are a content generation assistant. When users request content:

1. List available week folders using GET /api/weeks
2. Use specified week or ask which one to use
3. Generate content using POST /api/generate/blog or /api/generate/tweets
4. Always set return_content=true
5. Present results clearly formatted

API URL: https://your-app.onrender.com
```

### 5. Save and Test

1. Click "Save"
2. Choose visibility (Only me / Public)
3. Test: "List all week folders"

## Troubleshooting

### API Returns 403

- Verify service is "Public" in Render settings
- Check CustomGPT actions have Authentication: None
- Wait 30-60 seconds if service was sleeping (free tier)

### Schema Import Fails

- Verify `API_BASE_URL` is set in Render
- Check OpenAPI schema: `https://your-app.onrender.com/openapi.json`
- Manually configure actions instead

### Approval Required

CustomGPT may ask for approval before API calls. This is normal—click "Approve" when prompted.

### Quota Errors

If you see "insufficient_quota":
- Add payment method at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
- Add credits or set usage limits
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for details

## Updating Deployment

### Add New Week Folders

1. Add to `data/week-YYYY-MM-DD/` locally
2. Commit and push to GitHub
3. Render auto-deploys (if enabled)

### Update Code

1. Make changes locally
2. Commit and push to GitHub
3. Render auto-deploys

### Update Environment Variables

1. Render dashboard → Environment
2. Add/modify variables
3. Save (auto-redeploys)

## Cost Considerations

- **Render Free Tier**: 750 hours/month, services sleep after 15min
- **OpenAI API**: ~$0.25-$1.00 per blog post (GPT-4o)
- **Monitor usage**: Check OpenAI dashboard regularly

## Support

- Render docs: [render.com/docs](https://render.com/docs)
- CustomGPT docs: [platform.openai.com/docs/guides/custom-gpts](https://platform.openai.com/docs/guides/custom-gpts)
- Issues: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

