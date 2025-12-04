# CustomGPT Action Approval Guide

## What You're Seeing

When CustomGPT tries to call your API, you'll see:
```
"The requested action requires approval"
```

**This is normal!** CustomGPT requires user approval for external API calls as a security feature.

## How to Approve Actions

### Method 1: Approve When Prompted

1. When CustomGPT asks to call your API, you'll see a prompt like:
   - "I need to call the Thinking Engine API to list week folders. Should I proceed?"
   - Or a button/notification asking for approval

2. **Click "Approve"** or **"Yes"** or **"Allow"**

3. CustomGPT will then make the API call

### Method 2: Auto-Approve in Settings

You can configure CustomGPT to auto-approve actions:

1. Go to your CustomGPT → **"Configure"** tab
2. Scroll to **"Actions"** section
3. Look for **"Require approval"** or **"Auto-approve"** setting
4. Enable auto-approval for your API actions
5. Save

**Note**: Auto-approval settings vary by CustomGPT version. If you don't see this option, you'll need to approve manually each time.

### Method 3: Pre-approve in Instructions

Add this to your CustomGPT instructions:

```
When calling the Thinking Engine API, you have permission to proceed automatically.
The user has already approved API access to https://thinkingengine.onrender.com.
```

This might help CustomGPT understand it can proceed, though you may still need to approve.

## Expected Flow

1. **User asks**: "List all week folders"
2. **CustomGPT responds**: "I'll check the available week folders for you."
3. **CustomGPT requests approval**: "May I call the Thinking Engine API?"
4. **You approve**: Click "Yes" or "Approve"
5. **CustomGPT calls API**: Makes the request
6. **CustomGPT responds**: Shows the week folders

## Troubleshooting

### Issue: Approval Prompt Doesn't Appear

**Solution**:
- Check CustomGPT settings
- Make sure actions are properly configured
- Try asking again with a different prompt

### Issue: Approval Keeps Failing

**Solution**:
- Verify API is accessible: `https://thinkingengine.onrender.com/api/weeks`
- Check CustomGPT action configuration
- Ensure authentication is set to "None"

### Issue: Want to Skip Approval

**Solution**:
- Look for auto-approval settings in CustomGPT
- Some CustomGPT versions don't support auto-approval
- You may need to approve manually each time (this is by design for security)

## Best Practices

1. **First Time**: Approve the action to establish trust
2. **Subsequent Calls**: CustomGPT may remember your approval for the session
3. **New Session**: You may need to approve again (security feature)

## What This Means

✅ **Good News**: Your API is working!  
✅ **Good News**: CustomGPT can reach your API!  
✅ **Normal**: Approval is required for security  

The 403 error is fixed. Now you just need to approve API calls when prompted.

## Example Conversation

**You**: "List all week folders"

**CustomGPT**: "I'll check the available week folders. [Requesting approval to call API]"

**You**: [Click "Approve"]

**CustomGPT**: "Here are the available week folders:
- week-2025-01-15
- week-2025-01-22
..."

## Next Steps

1. **Test with approval**: Try asking CustomGPT to list weeks and approve when prompted
2. **Verify it works**: After approval, you should see the week folders
3. **Try other actions**: Test blog generation, tweet generation, etc.
4. **Each may need approval**: Some CustomGPT versions require approval per action type

---

**The API is working correctly!** The approval step is just CustomGPT's security feature. Once you approve, everything should work smoothly.

