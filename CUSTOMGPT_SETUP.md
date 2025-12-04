# CustomGPT Setup Guide

Complete step-by-step guide to set up CustomGPT with your Thinking Engine API deployed on Render.

## Prerequisites

✅ **API deployed on Render** - Your API should be live at `https://your-app.onrender.com`  
✅ **API is accessible** - Test by visiting `https://your-app.onrender.com/health`  
✅ **OpenAI account** - With ChatGPT Plus or Enterprise (required for CustomGPT)

---

## Step 1: Get Your API Information

### 1.1 Get Your Render API URL

After deploying to Render, you'll have a URL like:
```
https://thinking-engine-api.onrender.com
```

**Save this URL** - you'll need it in the next steps.

### 1.2 Get Your OpenAPI Schema URL

Your OpenAPI schema is available at:
```
https://your-app.onrender.com/openapi.json
```

**Test it**: Open this URL in your browser - you should see JSON schema.

### 1.3 Verify API is Working

Visit these URLs to verify:
- **Health check**: `https://your-app.onrender.com/health`
- **API docs**: `https://your-app.onrender.com/docs`
- **List weeks**: `https://your-app.onrender.com/api/weeks`

All should return valid responses.

---

## Step 2: Create Your CustomGPT

### 2.1 Open ChatGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Make sure you're logged in with a ChatGPT Plus or Enterprise account
3. Click on your profile name (bottom left)
4. Select **"My GPTs"** or **"Create a GPT"**

### 2.2 Start Creating

1. Click **"Create"** or **"Create a GPT"** button
2. You'll see the GPT Builder interface

---

## Step 3: Configure Basic Settings

### 3.1 Name and Description

In the **"Create"** tab:

- **Name**: `Thinking Engine` (or your preferred name)
- **Description**: `AI-powered content generator that creates blog posts and tweet ideas from curated research articles`
- **Instructions**: (We'll add this in Step 5)

### 3.2 Conversation Starters (Optional)

Add example prompts:
- "List all available week folders"
- "Generate a blog post for the latest week"
- "Create 30 tweet ideas for week-2025-01-15"

---

## Step 4: Configure Actions (API Integration)

This is the most important step!

### 4.1 Open Actions Tab

1. Click on the **"Configure"** tab (or "Actions" section)
2. Scroll down to **"Actions"** section
3. Click **"Create new action"**

### 4.2 Import OpenAPI Schema (Easiest Method)

1. In the **"Schema"** section, you'll see options
2. Select **"Import from URL"** or paste the schema
3. Enter your OpenAPI schema URL:
   ```
   https://your-app.onrender.com/openapi.json
   ```
4. Click **"Import"** or wait for it to auto-load

**What happens**: CustomGPT will automatically discover all your API endpoints!

### 4.3 Alternative: Manual Configuration

If automatic import doesn't work, manually add each action:

#### Action 1: List Week Folders
- **Name**: `List Week Folders`
- **Method**: `GET`
- **URL**: `https://your-app.onrender.com/api/weeks`
- **Description**: `Get all available week folders`

#### Action 2: Get Week Documents
- **Name**: `Get Week Documents`
- **Method**: `GET`
- **URL**: `https://your-app.onrender.com/api/weeks/{week_folder}/documents`
- **Description**: `Get documents in a specific week folder`
- **Parameters**: 
  - `week_folder` (path parameter, required)

#### Action 3: Generate Blog Post
- **Name**: `Generate Blog Post`
- **Method**: `POST`
- **URL**: `https://your-app.onrender.com/api/generate/blog`
- **Description**: `Generate a blog post from curated documents`
- **Body**:
  ```json
  {
    "week_folder": "{{week_folder}}",
    "return_content": true
  }
  ```

#### Action 4: Generate Tweet Ideas
- **Name**: `Generate Tweet Ideas`
- **Method**: `POST`
- **URL**: `https://your-app.onrender.com/api/generate/tweets`
- **Description**: `Generate tweet ideas from curated documents`
- **Body**:
  ```json
  {
    "week_folder": "{{week_folder}}",
    "count": {{count}},
    "return_content": true
  }
  ```

#### Action 5: Generate All
- **Name**: `Generate All Content`
- **Method**: `POST`
- **URL**: `https://your-app.onrender.com/api/generate/all`
- **Description**: `Generate both blog post and tweet ideas`
- **Body**:
  ```json
  {
    "week_folder": "{{week_folder}}",
    "tweet_count": {{tweet_count}},
    "return_content": true
  }
  ```

### 4.4 Authentication

For now, your API doesn't require authentication, so:
- Leave **"Authentication"** as **"None"** or **"No Auth"**

(If you add API key authentication later, configure it here)

---

## Step 5: Add Instructions

### 5.1 Go to Instructions Section

In the **"Create"** or **"Configure"** tab, find the **"Instructions"** field.

### 5.2 Add These Instructions

Copy and paste this (replace `your-app.onrender.com` with your actual URL):

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
https://your-app.onrender.com

## Example Interactions

User: "Generate a blog post for week-2025-01-15"
→ List weeks to verify it exists → Generate blog post → Present formatted result

User: "Create 30 tweet ideas"
→ List weeks → Use most recent week → Generate tweets → Present numbered list

User: "What week folders are available?"
→ List weeks → Present in a clear list
```

**Important**: Replace `your-app.onrender.com` with your actual Render URL!

---

## Step 6: Configure Additional Settings

### 6.1 Capabilities (Optional)

In the **"Configure"** tab:
- ✅ **Web Browsing**: Not needed (you have your own API)
- ✅ **Code Interpreter**: Not needed
- ✅ **DALL·E Image Generation**: Not needed

### 6.2 Knowledge (Optional)

You can upload files if you want, but it's not necessary since your data is in the API.

---

## Step 7: Save and Test

### 7.1 Save Your CustomGPT

1. Click **"Save"** button (top right)
2. Choose visibility:
   - **"Only me"** - Private, only you can use it
   - **"Anyone with a link"** - Shareable link
   - **"Public"** - Listed in GPT store (requires review)

3. Click **"Confirm"**

### 7.2 Test Your CustomGPT

1. Go to the **"Preview"** panel (right side)
2. Try these test prompts:

**Test 1: List Weeks**
```
List all available week folders
```

**Expected**: Should show list of week folders from your API

**Test 2: Generate Blog Post**
```
Generate a blog post for week-2025-01-15
```

**Expected**: Should generate and display a blog post

**Test 3: Generate Tweets**
```
Create 25 tweet ideas for the latest week
```

**Expected**: Should generate and display tweet ideas

### 7.3 Troubleshoot if Needed

If something doesn't work:

1. **Check API is accessible**: Visit `https://your-app.onrender.com/health`
2. **Check API logs**: Look at Render dashboard logs
3. **Verify URL in actions**: Make sure it's correct
4. **Test API directly**: Use `/docs` endpoint to test manually
5. **Check CustomGPT logs**: Look for error messages in the preview panel

---

## Step 8: Use Your CustomGPT

### 8.1 Access Your CustomGPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click on your profile → **"My GPTs"**
3. Find your **"Thinking Engine"** GPT
4. Click to open it

### 8.2 Start Using It

Now you can use natural language to interact:

**Examples:**
- "What week folders do you have?"
- "Generate a blog post for week-2025-01-15"
- "Create 30 tweet ideas for the latest week"
- "Show me what documents are in week-2025-01-15"
- "Generate both blog and tweets for week-2025-01-15"

The CustomGPT will:
1. Understand your request
2. Call the appropriate API endpoint
3. Format and present the results nicely

---

## Common Issues and Solutions

### Issue: "Failed to fetch" or Connection Error

**Solution:**
- Verify your Render service is running (check Render dashboard)
- Test the API URL directly in browser
- Check if service is sleeping (free tier sleeps after 15 min)
- Wait 30-60 seconds for first request after sleep

### Issue: "404 Not Found" for Week Folder

**Solution:**
- Verify the week folder exists in your GitHub `data/` directory
- Check the exact folder name (case-sensitive)
- List weeks first to see available options

### Issue: "500 Internal Server Error"

**Solution:**
- Check Render logs for detailed error
- Verify `OPENAI_API_KEY` is set in Render environment variables
- Test API directly using `/docs` endpoint

### Issue: CustomGPT Doesn't Call the API

**Solution:**
- Verify actions are configured correctly
- Check the OpenAPI schema imported correctly
- Review instructions - make sure they're clear about when to use API
- Try re-saving the CustomGPT

### Issue: API Returns Empty Results

**Solution:**
- Verify data files are committed to GitHub
- Check that week folders contain documents
- Test the API endpoint directly

---

## Updating Your CustomGPT

### When You Add New Week Folders

1. Add week folder to `data/` locally
2. Commit and push to GitHub
3. Render will auto-deploy (or manually redeploy)
4. Your CustomGPT will automatically see new weeks (no update needed!)

### When You Update API

1. Update code and deploy to Render
2. If API structure changes, update CustomGPT actions
3. If only logic changes, CustomGPT will work automatically

---

## Best Practices

1. **Test regularly** - Make sure API is working before using CustomGPT
2. **Monitor usage** - Check Render logs and OpenAI usage
3. **Keep instructions clear** - Update instructions if behavior changes
4. **Document your setup** - Note your Render URL and any customizations
5. **Backup your configuration** - Save your CustomGPT instructions somewhere

---

## Quick Reference

### Your API URLs
- **Base URL**: `https://your-app.onrender.com`
- **Health Check**: `https://your-app.onrender.com/health`
- **API Docs**: `https://your-app.onrender.com/docs`
- **OpenAPI Schema**: `https://your-app.onrender.com/openapi.json`

### Key Endpoints
- `GET /api/weeks` - List week folders
- `GET /api/weeks/{week_folder}/documents` - Get documents
- `POST /api/generate/blog` - Generate blog post
- `POST /api/generate/tweets` - Generate tweets
- `POST /api/generate/all` - Generate both

### Test Commands
```bash
# Test health
curl https://your-app.onrender.com/health

# List weeks
curl https://your-app.onrender.com/api/weeks

# Test blog generation (replace week folder)
curl -X POST https://your-app.onrender.com/api/generate/blog \
  -H "Content-Type: application/json" \
  -d '{"week_folder": "week-2025-01-15", "return_content": true}'
```

---

## Next Steps

✅ **You're all set!** Your CustomGPT is ready to use.

- Start generating content with natural language prompts
- Share your CustomGPT with others (if you made it public)
- Monitor usage and costs
- Add more week folders as needed

**Need help?** Check:
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Deployment details
- [CUSTOMGPT_GUIDE.md](CUSTOMGPT_GUIDE.md) - Detailed API guide
- Render Dashboard - Service logs and status

