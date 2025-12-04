# Complete Deployment & CustomGPT Setup Guide

**Complete step-by-step guide for deploying Thinking Engine to Render and using it with CustomGPT. No local setup required!**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Prepare Your GitHub Repository](#step-1-prepare-your-github-repository)
3. [Step 2: Deploy to Render](#step-2-deploy-to-render)
4. [Step 3: Configure Environment Variables](#step-3-configure-environment-variables)
5. [Step 4: Verify Deployment](#step-4-verify-deployment)
6. [Step 5: Set Up CustomGPT](#step-5-set-up-customgpt)
7. [Step 6: Test Your CustomGPT](#step-6-test-your-customgpt)
8. [Step 7: Using Your CustomGPT](#step-7-using-your-customgpt)
9. [Troubleshooting](#troubleshooting)
10. [Updating Your Deployment](#updating-your-deployment)

---

## Prerequisites

Before you begin, make sure you have:

1. ✅ **GitHub Account** - Sign up at [github.com](https://github.com) (free)
2. ✅ **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. ✅ **OpenAI Account** - With ChatGPT Plus or Enterprise subscription
4. ✅ **OpenAI API Key** - Get it from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Getting Your OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign in or create an account
3. Click on your profile (top right) → **"API keys"**
4. Click **"Create new secret key"**
5. **Copy the key immediately** (you won't see it again!)
6. Save it somewhere safe - you'll need it in Step 3

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Create a New GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in the details:
   - **Repository name**: `thinking-engine` (or your preferred name)
   - **Description**: "AI Content Thinking Engine API"
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** check "Initialize with README" (we already have files)
4. Click **"Create repository"**

### 1.2 Upload Your Project Files

You have two options:

#### Option A: Using GitHub Web Interface (Easiest)

1. On your new repository page, you'll see instructions
2. Click **"uploading an existing file"** link
3. Drag and drop ALL files from your project folder:
   - `src/` folder (entire folder)
   - `data/` folder (entire folder with week folders)
   - `requirements.txt`
   - `render.yaml`
   - `Procfile`
   - `run_api.py`
   - `runtime.txt`
   - `README.md`
   - All `.md` documentation files
   - **Everything except** `venv/`, `__pycache__/`, `.env`, `output/`
4. Scroll down and click **"Commit changes"**

#### Option B: Using Git Command Line (If you have Git installed)

```bash
# Navigate to your project folder
cd /path/to/thinkingengine

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Thinking Engine API"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/thinking-engine.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important**: Make sure your `data/` folder with week folders is included!

### 1.3 Verify Files Are Uploaded

1. Go to your GitHub repository page
2. Check that you can see:
   - ✅ `src/` folder
   - ✅ `data/` folder (with week folders inside)
   - ✅ `requirements.txt`
   - ✅ `render.yaml`
   - ✅ `Procfile`
   - ✅ `run_api.py`

If all files are there, you're ready for the next step!

---

## Step 2: Deploy to Render

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up with your GitHub account (recommended) or email
4. Verify your email if required

### 2.2 Connect GitHub (If Not Already Connected)

1. In Render dashboard, go to **"Account Settings"**
2. Click **"Connect GitHub"** or **"GitHub"** tab
3. Authorize Render to access your GitHub repositories
4. Select which repositories to allow (or all repositories)

### 2.3 Create New Web Service

You have two options:

#### Option A: Using Blueprint (Easiest - Recommended)

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Blueprint"**
3. Render will show your GitHub repositories
4. Find and select your `thinking-engine` repository
5. Render will automatically detect `render.yaml`
6. You'll see a preview of the service configuration
7. Click **"Apply"** or **"Create Blueprint"**

#### Option B: Manual Setup

1. In Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Click **"Connect account"** if GitHub isn't connected
4. Find and select your `thinking-engine` repository
5. Click **"Connect"**

### 2.4 Configure Service Settings

If using manual setup, configure these settings:

- **Name**: `thinking-engine-api` (or your preferred name)
- **Environment**: Select **"Python 3"**
- **Region**: Choose closest to you (e.g., "Oregon (US West)")
- **Branch**: `main` (or `master` if that's your default)
- **Root Directory**: Leave empty (default)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python run_api.py`
- **Instance Type**: **Free** (or upgrade if needed)

### 2.5 Advanced Settings

Click **"Advanced"** and set:

- **Health Check Path**: `/health`
- **Auto-Deploy**: **Yes** (deploys automatically on git push)

Click **"Create Web Service"**

### 2.6 Wait for Deployment

Render will now:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Start your API server

**This takes 2-5 minutes**. You'll see build logs in real-time.

**Don't close the page!** Wait for deployment to complete.

---

## Step 3: Configure Environment Variables

### 3.1 Add OpenAI API Key

1. In your Render service dashboard, go to **"Environment"** tab (left sidebar)
2. Click **"Add Environment Variable"**
3. Fill in:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Paste your OpenAI API key (the one you saved earlier)
   - **Mark as Secret**: ✅ Check this box (important!)
4. Click **"Save Changes"**

### 3.2 Add Optional Environment Variables (Recommended)

Add these for better control:

1. **OPENAI_MODEL**
   - Key: `OPENAI_MODEL`
   - Value: `gpt-4o`
   - Secret: No

2. **MAX_CHARS_PER_DOCUMENT** (Optional)
   - Key: `MAX_CHARS_PER_DOCUMENT`
   - Value: `12000`
   - Secret: No

3. **MAX_TOTAL_CONTEXT_CHARS** (Optional)
   - Key: `MAX_TOTAL_CONTEXT_CHARS`
   - Value: `50000`
   - Secret: No

### 3.3 Save and Redeploy

After adding environment variables:
1. Click **"Save Changes"**
2. Render will automatically redeploy your service
3. Wait for redeployment to complete (1-2 minutes)

---

## Step 4: Verify Deployment

### 4.1 Get Your API URL

1. In Render dashboard, your service should show **"Live"** status
2. You'll see a URL like: `https://thinking-engine-api.onrender.com`
3. **Copy this URL** - you'll need it for CustomGPT!

### 4.2 Test Health Endpoint

1. Open a new browser tab
2. Go to: `https://your-app-name.onrender.com/health`
3. You should see:
   ```json
   {
     "status": "healthy",
     "data_directory_exists": true,
     "api_key_configured": true,
     "version": "0.1.0"
   }
   ```

If you see this, your API is working! ✅

### 4.3 Test API Documentation

1. Go to: `https://your-app-name.onrender.com/docs`
2. You should see interactive API documentation (Swagger UI)
3. This confirms your API is fully deployed

### 4.4 Test List Weeks Endpoint

1. Go to: `https://your-app-name.onrender.com/api/weeks`
2. You should see a list of your week folders:
   ```json
   {
     "week_folders": ["week-2025-01-15", ...],
     "count": 1
   }
   ```

If this works, you're ready for CustomGPT! ✅

### 4.5 Common Issues

**Issue**: Health check shows `"api_key_configured": false`
- **Solution**: Go back to Step 3 and verify `OPENAI_API_KEY` is set correctly

**Issue**: Health check shows `"data_directory_exists": false`
- **Solution**: Verify `data/` folder is in your GitHub repository

**Issue**: Service shows "Build Failed"
- **Solution**: Check build logs for errors, verify `requirements.txt` is correct

---

## Step 5: Set Up CustomGPT

### 5.1 Open ChatGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Sign in with your OpenAI account
3. Make sure you have **ChatGPT Plus** or **Enterprise** subscription
   - CustomGPT requires a paid subscription

### 5.2 Create New CustomGPT

1. Click on your **profile name** (bottom left corner)
2. Select **"My GPTs"** or **"Create a GPT"**
3. Click **"Create"** or **"Create a GPT"** button

### 5.3 Configure Basic Information

In the **"Create"** tab:

1. **Name**: Enter `Thinking Engine` (or your preferred name)
2. **Description**: 
   ```
   AI-powered content generator that creates blog posts and tweet ideas 
   from curated research articles organized by week.
   ```

3. **Instructions**: (We'll add this in Step 5.6)

### 5.4 Add Conversation Starters (Optional but Recommended)

Click **"Conversation starters"** and add:
- `"List all available week folders"`
- `"Generate a blog post for the latest week"`
- `"Create 30 tweet ideas for week-2025-01-15"`

### 5.5 Configure Actions (API Integration)

This is the most important step!

1. Click on the **"Configure"** tab (top of the page)
2. Scroll down to the **"Actions"** section
3. Click **"Create new action"** or **"Add action"**

#### Method 1: Import OpenAPI Schema (Easiest)

1. In the **"Schema"** section, you'll see a text area
2. Look for **"Import from URL"** option or paste the schema URL
3. Enter your OpenAPI schema URL:
   ```
   https://your-app-name.onrender.com/openapi.json
   ```
   (Replace `your-app-name` with your actual Render app name)

4. Click **"Import"** or wait for it to auto-load
5. CustomGPT will automatically discover all your API endpoints!

**What you should see**: A list of available actions like:
- `list_week_folders`
- `get_week_documents`
- `generate_blog`
- `generate_tweets`
- `generate_all`

#### Method 2: Manual Configuration (If Import Doesn't Work)

If automatic import doesn't work, add each action manually:

**Action 1: List Week Folders**
- Click **"Create new action"**
- **Name**: `List Week Folders`
- **Description**: `Get all available week folders from the API`
- **Method**: `GET`
- **URL**: `https://your-app-name.onrender.com/api/weeks`
- Click **"Save"**

**Action 2: Get Week Documents**
- Click **"Create new action"**
- **Name**: `Get Week Documents`
- **Description**: `Get documents in a specific week folder`
- **Method**: `GET`
- **URL**: `https://your-app-name.onrender.com/api/weeks/{week_folder}/documents`
- **Parameters**: 
  - Add parameter: `week_folder` (path parameter, required, string)
- Click **"Save"**

**Action 3: Generate Blog Post**
- Click **"Create new action"**
- **Name**: `Generate Blog Post`
- **Description**: `Generate a blog post from curated documents`
- **Method**: `POST`
- **URL**: `https://your-app-name.onrender.com/api/generate/blog`
- **Body** (click "Add body parameter"):
  ```json
  {
    "week_folder": "{{week_folder}}",
    "return_content": true
  }
  ```
- Click **"Save"**

**Action 4: Generate Tweet Ideas**
- Click **"Create new action"**
- **Name**: `Generate Tweet Ideas`
- **Description**: `Generate tweet ideas from curated documents`
- **Method**: `POST`
- **URL**: `https://your-app-name.onrender.com/api/generate/tweets`
- **Body**:
  ```json
  {
    "week_folder": "{{week_folder}}",
    "count": {{count}},
    "return_content": true
  }
  ```
- Click **"Save"**

**Action 5: Generate All**
- Click **"Create new action"**
- **Name**: `Generate All Content`
- **Description**: `Generate both blog post and tweet ideas`
- **Method**: `POST`
- **URL**: `https://your-app-name.onrender.com/api/generate/all`
- **Body**:
  ```json
  {
    "week_folder": "{{week_folder}}",
    "tweet_count": {{tweet_count}},
    "return_content": true
  }
  ```
- Click **"Save"**

### 5.6 Add Instructions

1. In the **"Configure"** tab, find the **"Instructions"** field (large text area)
2. Copy and paste this (replace `your-app-name.onrender.com` with your actual URL):

```
You are a content generation assistant powered by the Thinking Engine API.

Your role is to help users generate blog posts and tweet ideas from curated research articles organized by week.

## How to Use the API

1. **When a user asks to generate content:**
   - First, list available week folders using GET /api/weeks
   - If the user specifies a week folder, use it directly
   - If not specified, ask which week folder to use, or use the most recent one

2. **For blog posts:**
   - Use POST /api/generate/blog with the week_folder parameter
   - Always set return_content=true to get the full blog post content
   - Present the blog post in a well-formatted markdown style
   - Highlight any fact-check issues if present

3. **For tweet ideas:**
   - Use POST /api/generate/tweets with week_folder and count parameters
   - Default count is 25, but adjust based on user request
   - Always set return_content=true
   - Present tweets in a numbered list with hashtags and sources

4. **For both blog and tweets:**
   - Use POST /api/generate/all with week_folder and tweet_count parameters
   - Present both results clearly separated

## Important Guidelines

- Always verify the week folder exists before generating content
- If a week folder doesn't exist, inform the user and list available options
- Present content in a clear, readable format
- Include source information when available
- If fact-check issues are found, mention them to the user
- Be helpful and conversational - explain what you're doing

## API Base URL
https://your-app-name.onrender.com

## Example Interactions

User: "Generate a blog post for week-2025-01-15"
→ List weeks to verify it exists → Generate blog post → Present formatted result

User: "Create 30 tweet ideas"
→ List weeks → Use most recent week → Generate tweets → Present numbered list

User: "What week folders are available?"
→ List weeks → Present in a clear list
```

**Important**: Replace `your-app-name.onrender.com` with your actual Render URL!

3. Scroll down and make sure instructions are saved

### 5.7 Configure Additional Settings

1. **Capabilities** (in Configure tab):
   - ✅ **Web Browsing**: Not needed (uncheck if checked)
   - ✅ **Code Interpreter**: Not needed (uncheck if checked)
   - ✅ **DALL·E Image Generation**: Not needed (uncheck if checked)

2. **Knowledge** (optional):
   - You can skip this - your data is in the API

### 5.8 Save Your CustomGPT

1. Click **"Save"** button (top right corner)
2. Choose visibility:
   - **"Only me"** - Private, only you can use it
   - **"Anyone with a link"** - Shareable with link
   - **"Public"** - Listed in GPT store (requires review)
3. Click **"Confirm"**

Your CustomGPT is now created! 🎉

---

## Step 6: Test Your CustomGPT

### 6.1 Open Your CustomGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click your profile → **"My GPTs"**
3. Find your **"Thinking Engine"** GPT
4. Click to open it

### 6.2 Test Basic Functionality

Try these test prompts one by one:

#### Test 1: List Week Folders
```
List all available week folders
```

**Expected Result**: Should show a list of week folders from your API

**If it works**: ✅ Great! Move to next test.

**If it doesn't work**: 
- Check that your Render API is accessible
- Verify the API URL in CustomGPT actions is correct
- Check Render service is not sleeping

#### Test 2: Get Week Documents
```
What documents are in week-2025-01-15?
```
(Replace with your actual week folder name)

**Expected Result**: Should show list of documents in that week folder

#### Test 3: Generate Blog Post
```
Generate a blog post for week-2025-01-15
```

**Expected Result**: Should generate and display a formatted blog post

**This may take 30-60 seconds** - be patient!

#### Test 4: Generate Tweet Ideas
```
Create 25 tweet ideas for the latest week
```

**Expected Result**: Should generate and display a numbered list of tweet ideas

### 6.3 Troubleshoot if Needed

If tests fail, see [Troubleshooting](#troubleshooting) section below.

---

## Step 7: Using Your CustomGPT

### 7.1 Access Your CustomGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click your profile → **"My GPTs"**
3. Click on **"Thinking Engine"** to open it

### 7.2 Example Prompts You Can Use

**List Available Weeks:**
```
What week folders do you have?
List all available weeks
Show me all week folders
```

**Generate Blog Post:**
```
Generate a blog post for week-2025-01-15
Create a blog post for the latest week
Write a blog post for week-2025-01-15
```

**Generate Tweet Ideas:**
```
Create 30 tweet ideas for week-2025-01-15
Generate 25 tweets for the latest week
Give me tweet ideas for week-2025-01-15
```

**Generate Both:**
```
Generate both blog and tweets for week-2025-01-15
Create blog post and tweet ideas for the latest week
```

**Get Document Information:**
```
What documents are in week-2025-01-15?
Show me the sources for week-2025-01-15
```

### 7.3 How It Works

1. You type a natural language request
2. CustomGPT understands what you want
3. CustomGPT calls your Render API
4. API processes the request and generates content
5. CustomGPT formats and presents the results

**That's it!** No coding, no local setup - just natural language!

---

## Troubleshooting

### CustomGPT Can't Connect to API

**Symptoms**: 
- "Failed to fetch" error
- "Connection error" message
- Actions don't work

**Solutions**:
1. **Check Render service is running**:
   - Go to Render dashboard
   - Verify service shows "Live" status
   - If "Sleeping", wait 30-60 seconds for it to wake up

2. **Test API directly**:
   - Visit: `https://your-app.onrender.com/health`
   - Should return JSON with `"status": "healthy"`

3. **Verify API URL in CustomGPT**:
   - Go to CustomGPT → Configure → Actions
   - Check all URLs start with `https://your-app.onrender.com`
   - Make sure there are no typos

4. **Check CORS settings**:
   - API should allow all origins (already configured)
   - If you changed CORS, revert it

### API Returns 404 Errors

**Symptoms**:
- "Week folder not found" errors
- 404 responses

**Solutions**:
1. **Verify week folder exists**:
   - Test: `https://your-app.onrender.com/api/weeks`
   - Check the folder name matches exactly (case-sensitive)

2. **Check data files in GitHub**:
   - Verify `data/` folder is in your repository
   - Verify week folders are inside `data/`

### API Returns 500 Errors

**Symptoms**:
- Internal server errors
- "Something went wrong" messages

**Solutions**:
1. **Check Render logs**:
   - Go to Render dashboard → Your service → Logs
   - Look for error messages
   - Common issues: Missing API key, import errors

2. **Verify environment variables**:
   - Go to Render → Environment tab
   - Verify `OPENAI_API_KEY` is set correctly
   - Check it's marked as "Secret"

3. **Test API key**:
   - Make sure your OpenAI API key is valid
   - Check you have credits in your OpenAI account

### Service is Slow

**Symptoms**:
- Requests take 30-60 seconds
- Timeout errors

**Solutions**:
1. **First request after sleep** (Free tier):
   - Render free tier services sleep after 15 min inactivity
   - First request takes 30-60 seconds to wake up
   - This is normal - wait for it

2. **Upgrade to paid tier**:
   - Paid tier keeps services always-on
   - No wake-up delay

3. **Large documents**:
   - Processing large documents takes time
   - This is expected - be patient

### CustomGPT Doesn't Call API

**Symptoms**:
- CustomGPT responds but doesn't use API
- No API calls in logs

**Solutions**:
1. **Check actions are configured**:
   - Go to CustomGPT → Configure → Actions
   - Verify actions are listed and enabled

2. **Check instructions**:
   - Make sure instructions clearly tell when to use API
   - Add explicit examples

3. **Test actions manually**:
   - In CustomGPT preview, try explicit prompts
   - "Use the API to list week folders"

### Build Fails on Render

**Symptoms**:
- Deployment shows "Build Failed"
- Service won't start

**Solutions**:
1. **Check build logs**:
   - Go to Render → Logs tab
   - Look for error messages
   - Common: Missing dependencies, Python version issues

2. **Verify requirements.txt**:
   - Make sure all dependencies are listed
   - Check for typos in package names

3. **Check Python version**:
   - Verify `runtime.txt` specifies Python 3.11
   - Or remove it to use Render's default

---

## Updating Your Deployment

### Adding New Week Folders

1. **Add week folder locally** (or directly on GitHub):
   - Create folder: `data/week-YYYY-MM-DD/`
   - Add article files inside

2. **Commit to GitHub**:
   - If using GitHub web interface:
     - Go to your repository
     - Click "Add file" → "Upload files"
     - Upload your new week folder
     - Commit changes
   - If using Git:
     ```bash
     git add data/week-YYYY-MM-DD/
     git commit -m "Add week YYYY-MM-DD"
     git push origin main
     ```

3. **Render auto-deploys**:
   - If auto-deploy is enabled, Render will redeploy automatically
   - New week folder will be available immediately

### Updating Code

1. **Make changes** to your code
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update code"
   git push origin main
   ```
3. **Render auto-deploys** (if enabled)
4. **Or manually redeploy** from Render dashboard

### Updating Environment Variables

1. Go to Render dashboard → Your service → Environment
2. Add or modify environment variables
3. Click "Save Changes"
4. Render will automatically redeploy

---

## Important Notes

### Free Tier Limitations

- **Service Sleep**: Services sleep after 15 minutes of inactivity
- **Wake-up Time**: First request after sleep takes 30-60 seconds
- **Monthly Hours**: 750 hours/month free
- **Upgrade**: Consider paid tier for always-on service

### API Costs

- **OpenAI API**: Charges per token used
- **Monitor Usage**: Check [platform.openai.com/usage](https://platform.openai.com/usage)
- **Typical Cost**: $2-5 per blog post generation
- **Set Limits**: Consider setting usage limits in OpenAI dashboard

### Data Files

- **Stored in GitHub**: Data files are in your GitHub repository
- **Read-Only on Render**: Render reads from GitHub (read-only)
- **Updates**: Commit new data to GitHub, Render will see it
- **Output Files**: Generated files are ephemeral (lost on redeploy)

### Security

- **API Keys**: Stored securely in Render (marked as secrets)
- **No Authentication**: API is currently public (add auth if needed)
- **CORS**: Configured to allow CustomGPT access
- **HTTPS**: All Render URLs use HTTPS (secure)

---

## Quick Reference

### Your Important URLs

- **Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
- **Your API**: `https://your-app-name.onrender.com`
- **API Health**: `https://your-app-name.onrender.com/health`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **OpenAPI Schema**: `https://your-app-name.onrender.com/openapi.json`
- **CustomGPT**: [chat.openai.com](https://chat.openai.com) → My GPTs

### Key Endpoints

- `GET /health` - Health check
- `GET /api/weeks` - List week folders
- `GET /api/weeks/{week}/documents` - Get documents
- `POST /api/generate/blog` - Generate blog post
- `POST /api/generate/tweets` - Generate tweets
- `POST /api/generate/all` - Generate both

### Support Resources

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **CustomGPT Docs**: [platform.openai.com/docs/guides/custom-gpts](https://platform.openai.com/docs/guides/custom-gpts)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## Success Checklist

✅ GitHub repository created and files uploaded  
✅ Render account created and service deployed  
✅ Environment variables configured (OPENAI_API_KEY)  
✅ API health check passes  
✅ CustomGPT created and configured  
✅ Actions imported/configured correctly  
✅ Instructions added to CustomGPT  
✅ Test prompts work successfully  

**If all checked, you're all set!** 🎉

---

## Next Steps

1. **Start using your CustomGPT** for content generation
2. **Add more week folders** as you curate new articles
3. **Monitor usage** in Render and OpenAI dashboards
4. **Share your CustomGPT** with others (if you made it public)
5. **Consider upgrades** if you need always-on service

**Enjoy your Thinking Engine!** 🚀

