# Deployment Checklist

Use this checklist when deploying to Render for CustomGPT integration.

## Pre-Deployment

- [ ] **Data files committed to GitHub**
  - Verify `data/` directory is NOT in `.gitignore`
  - All week folders are committed: `git add data/ && git commit -m "Add data files"`
  - Push to GitHub: `git push origin main`

- [ ] **Environment variables ready**
  - OpenAI API key obtained
  - Optional: Model preference (default: gpt-4o)
  - Optional: Document limits configured

- [ ] **Code is ready**
  - All changes committed
  - Tests pass locally (if applicable)
  - `requirements.txt` is up to date

## Render Setup

- [ ] **Create Render account**
  - Sign up at [render.com](https://render.com)
  - Connect GitHub account

- [ ] **Deploy service**
  - Option A: Use `render.yaml` (Blueprint)
  - Option B: Manual setup with `Procfile`
  - Set build command: `pip install -r requirements.txt`
  - Set start command: `python run_api.py`
  - Set health check: `/health`

- [ ] **Configure environment variables**
  - `OPENAI_API_KEY` (required, mark as secret)
  - `OPENAI_MODEL` (optional, default: gpt-4o)
  - `MAX_CHARS_PER_DOCUMENT` (optional, default: 12000)
  - `MAX_TOTAL_CONTEXT_CHARS` (optional, default: 50000)

- [ ] **Verify deployment**
  - Check build logs for errors
  - Test health endpoint: `https://your-app.onrender.com/health`
  - Test API docs: `https://your-app.onrender.com/docs`
  - Test list weeks: `https://your-app.onrender.com/api/weeks`

## CustomGPT Configuration

- [ ] **Get OpenAPI schema**
  - Visit: `https://your-app.onrender.com/openapi.json`
  - Copy the URL

- [ ] **Create/Edit CustomGPT**
  - Go to ChatGPT → Create Custom GPT
  - Navigate to Actions section

- [ ] **Configure Actions**
  - Import OpenAPI schema from URL
  - OR manually add endpoints (see RENDER_DEPLOYMENT.md)

- [ ] **Add instructions**
  - Copy instructions from RENDER_DEPLOYMENT.md
  - Update API URL in instructions
  - Save CustomGPT

- [ ] **Test CustomGPT**
  - "List all week folders"
  - "Generate blog post for week-2025-01-15"
  - "Create 30 tweet ideas for latest week"

## Post-Deployment

- [ ] **Monitor service**
  - Check Render dashboard for service status
  - Monitor logs for errors
  - Verify health checks are passing

- [ ] **Update data files (when needed)**
  - Add new week folders to `data/` locally
  - Commit and push to GitHub
  - Render will auto-deploy (or manually redeploy)

- [ ] **Document your setup**
  - Note your Render service URL
  - Document any custom configurations
  - Share with team if applicable

## Troubleshooting

If something doesn't work:

1. **Check Render logs** - Look for build/runtime errors
2. **Test API directly** - Use `/docs` endpoint to test
3. **Verify environment variables** - All required vars set?
4. **Check data files** - Are they in the repository?
5. **Test locally first** - Run `python run_api.py` locally

## Quick Commands

```bash
# Test API locally
python run_api.py

# Check health
curl http://localhost:8000/health

# List weeks
curl http://localhost:8000/api/weeks

# After deployment, test remotely
curl https://your-app.onrender.com/health
```

## Support Resources

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **CustomGPT Guide**: See RENDER_DEPLOYMENT.md
- **Local Setup**: See CUSTOMGPT_GUIDE.md

