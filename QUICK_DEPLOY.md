# Quick Deploy Guide - 5 Steps to Get Running

**Fastest way to deploy and use Thinking Engine with CustomGPT**

---

## Prerequisites (5 minutes)

1. **GitHub Account**: [github.com/signup](https://github.com/signup)
2. **Render Account**: [render.com](https://render.com) - Sign up with GitHub
3. **OpenAI Account**: [platform.openai.com](https://platform.openai.com) - Get API key
4. **ChatGPT Plus**: Required for CustomGPT

---

## Step 1: Upload to GitHub (2 minutes)

1. Create new repository on GitHub
2. Upload ALL project files (drag & drop)
3. **Important**: Include `data/` folder with week folders!

---

## Step 2: Deploy to Render (3 minutes)

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Select your repository
4. Click **"Apply"**
5. Wait for deployment (2-5 minutes)

---

## Step 3: Add API Key (1 minute)

1. In Render dashboard → Your service → **"Environment"**
2. Add: `OPENAI_API_KEY` = (your OpenAI API key)
3. Mark as **Secret** ✅
4. Save (auto-redeploys)

---

## Step 4: Get Your API URL (30 seconds)

1. Copy your Render URL: `https://your-app.onrender.com`
2. Test it: Visit `https://your-app.onrender.com/health`
3. Should show: `{"status": "healthy", ...}`

---

## Step 5: Set Up CustomGPT (5 minutes)

1. Go to [chat.openai.com](https://chat.openai.com) → **"My GPTs"** → **"Create"**
2. **Name**: `Thinking Engine`
3. **Configure tab** → **"Actions"** → **"Create new action"**
4. **Import schema**: `https://your-app.onrender.com/openapi.json`
5. **Instructions** (paste this, replace URL):
   ```
   You are a content generation assistant. When users ask to generate content:
   1. List week folders using GET /api/weeks
   2. Use specified week or ask which one
   3. Generate using POST /api/generate/blog, /api/generate/tweets, or /api/generate/all
   4. Always set return_content=true
   5. Present results clearly formatted
   
   API URL: https://your-app.onrender.com
   ```
6. **Save** → Choose visibility → **"Confirm"**

---

## ✅ Done! Test It

Open your CustomGPT and try:
- `"List all week folders"`
- `"Generate a blog post for week-2025-01-15"`

---

## 🆘 Quick Troubleshooting

**API not working?**
- Check Render service is "Live"
- Verify `OPENAI_API_KEY` is set
- Test: `https://your-app.onrender.com/health`

**CustomGPT can't connect?**
- Verify API URL in actions is correct
- Check Render service isn't sleeping (wait 30-60 sec)

**Need more help?**
- See [COMPLETE_DEPLOYMENT_GUIDE.md](COMPLETE_DEPLOYMENT_GUIDE.md) for detailed steps

---

**Total time: ~15 minutes** ⏱️

