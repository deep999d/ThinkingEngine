# Fix: CustomGPT "Could not find a valid URL in servers" Error

## Problem

When importing the OpenAPI schema into CustomGPT, you get this error:
```
Could not find a valid URL in `servers`
```

## Solution

The OpenAPI schema needs a `servers` field that tells CustomGPT where your API is located.

### Step 1: Get Your Render URL

After deploying to Render, you'll have a URL like:
```
https://your-app-name.onrender.com
```

**Copy this URL** - you'll need it in the next step.

### Step 2: Set API_BASE_URL Environment Variable

1. Go to your Render dashboard
2. Select your service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `API_BASE_URL`
   - **Value**: `https://your-app-name.onrender.com` (your actual Render URL)
   - **Secret**: No (unchecked)
6. Click **"Save Changes"**

Render will automatically redeploy your service.

### Step 3: Verify OpenAPI Schema

1. Wait for redeployment to complete (1-2 minutes)
2. Visit: `https://your-app-name.onrender.com/openapi.json`
3. Look for the `servers` field at the top:
   ```json
   {
     "openapi": "3.1.0",
     "info": {...},
     "servers": [
       {
         "url": "https://your-app-name.onrender.com",
         "description": "Production server"
       }
     ],
     "paths": {...}
   }
   ```

If you see the `servers` field with your URL, it's fixed! ✅

### Step 4: Import into CustomGPT

1. Go to CustomGPT → Configure → Actions
2. Import from URL: `https://your-app-name.onrender.com/openapi.json`
3. It should now work without the error!

## Alternative: Manual Configuration

If you prefer not to set the environment variable, you can manually configure each action in CustomGPT:

1. Don't import the schema
2. Manually add each action with the full URL:
   - `https://your-app-name.onrender.com/api/weeks`
   - `https://your-app-name.onrender.com/api/generate/blog`
   - etc.

## Verification

To verify the fix worked:

1. Check OpenAPI schema has `servers` field
2. Import into CustomGPT - no error should appear
3. Test an action - it should call your API successfully

## Notes

- The `API_BASE_URL` environment variable is optional but recommended
- If not set, the schema will have a placeholder URL
- Always use your actual Render URL (not the placeholder)
- The URL must include `https://` protocol

