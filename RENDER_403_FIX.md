# Fix: 403 Forbidden Error from Render

## Problem

CustomGPT is getting a 403 Forbidden error when trying to call your API:
```
[debug] Function Call (Internal or External) Had a 403 Status Code
Error talking to connector
```

## Possible Causes

1. **Render Security Settings** - Render might be blocking requests
2. **Missing CORS Headers** - Though we've configured CORS
3. **Render Free Tier Restrictions** - Some limitations on free tier
4. **Request Headers** - CustomGPT might be sending headers Render doesn't like

## Solutions

### Solution 1: Verify API is Publicly Accessible

1. **Test in Browser**:
   - Open: `https://thinkingengine.onrender.com/health`
   - Should return JSON, not an error page
   - If you see an error page, Render might be blocking

2. **Test with curl**:
   ```bash
   curl -v https://thinkingengine.onrender.com/health
   ```
   - Check the response code
   - Should be 200, not 403

### Solution 2: Check Render Service Settings

1. Go to Render Dashboard → Your Service
2. Check **"Settings"** tab
3. Look for:
   - **"Public"** setting - should be enabled
   - **"Auto-Deploy"** - doesn't affect this but good to check
   - Any **"Security"** or **"Access"** settings

### Solution 3: Verify Environment Variables

Make sure these are set in Render:
- `OPENAI_API_KEY` - Required
- `API_BASE_URL` - Should be `https://thinkingengine.onrender.com`

### Solution 4: Try Different Endpoint

Instead of `/health`, try:
- `https://thinkingengine.onrender.com/` (root endpoint)
- `https://thinkingengine.onrender.com/api/weeks`

In CustomGPT, you can manually configure actions to use these endpoints.

### Solution 5: Check Render Logs

1. Go to Render Dashboard → Your Service → **"Logs"**
2. Look for:
   - 403 errors
   - Security-related messages
   - Blocked requests

### Solution 6: Render Free Tier Limitations

Render's free tier might have some restrictions:
- **Solution**: Consider upgrading to paid tier if needed
- Or wait a few minutes and try again (rate limiting)

### Solution 7: Manual Action Configuration

Instead of importing OpenAPI schema, manually configure each action:

1. In CustomGPT → Configure → Actions
2. Don't import schema
3. Manually add each action:
   - **List Weeks**: `GET https://thinkingengine.onrender.com/api/weeks`
   - **Generate Blog**: `POST https://thinkingengine.onrender.com/api/generate/blog`
   - etc.

### Solution 8: Check CustomGPT Action Configuration

1. In CustomGPT → Configure → Actions
2. Check if **"Authentication"** is set
3. If it's set to "API Key" or similar, change to **"None"**
4. Our API doesn't require authentication

### Solution 9: Test API Directly

Use a tool like Postman or curl to test:

```bash
# Test health endpoint
curl -X GET https://thinkingengine.onrender.com/health \
  -H "Accept: application/json" \
  -H "User-Agent: CustomGPT"

# Test list weeks
curl -X GET https://thinkingengine.onrender.com/api/weeks \
  -H "Accept: application/json"
```

If these work but CustomGPT doesn't, it's a CustomGPT-specific issue.

### Solution 10: Update Code and Redeploy

The code has been updated with:
- Better CORS handling
- Explicit OPTIONS handler
- CORS headers on all responses

1. **Commit the updated code**:
   ```bash
   git add src/thinking_engine/api.py
   git commit -m "Fix CORS and add explicit headers for CustomGPT"
   git push origin main
   ```

2. **Wait for Render to redeploy** (auto-deploy if enabled)

3. **Test again** in CustomGPT

## Verification Steps

After trying solutions:

1. ✅ API is accessible in browser
2. ✅ API returns 200 (not 403) with curl
3. ✅ CORS headers are present in response
4. ✅ CustomGPT actions are configured without authentication
5. ✅ Render service is "Live" (not sleeping)

## Still Not Working?

If you've tried all solutions:

1. **Check Render Status**: [status.render.com](https://status.render.com)
2. **Contact Render Support**: They can check if requests are being blocked
3. **Try Alternative**: Use ngrok or another service temporarily to test
4. **Check CustomGPT Logs**: Look for more detailed error messages

## Alternative: Use ngrok for Testing

If Render continues to block, you can use ngrok temporarily:

1. Run API locally: `python run_api.py`
2. Use ngrok: `ngrok http 8000`
3. Use ngrok URL in CustomGPT: `https://abc123.ngrok.io`
4. This helps determine if it's a Render-specific issue

## Expected Behavior

After fixes, CustomGPT should:
- Successfully call `/health` endpoint
- Get 200 response with JSON
- Be able to call other endpoints
- Generate content successfully

---

**Note**: The code has been updated with improved CORS handling. Make sure to redeploy after pulling the latest changes.

