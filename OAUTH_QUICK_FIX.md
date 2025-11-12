# Fix "invalid_grant" Error - Google OAuth Setup

## The Problem:
`❌ Authentication error: (invalid_grant) Bad Request`

This means your Google OAuth credentials aren't set up correctly or don't exist yet.

---

## 5-Minute Fix:

### Step 1: Go to Google Cloud Console
👉 **[console.cloud.google.com](https://console.cloud.google.com)**

### Step 2: Create Project (if you haven't)
1. Click **"Select a project"** dropdown (top bar)
2. Click **"New Project"**
3. Name: `Project Veritas`
4. Click **"Create"**
5. Wait 10 seconds, then select the project

### Step 3: Enable Google+ API
1. Go to: **"APIs & Services"** → **"Library"** (left sidebar)
2. Search: `Google+ API`
3. Click on it
4. Click **"Enable"**

### Step 4: Configure OAuth Consent Screen
1. Go to: **"APIs & Services"** → **"OAuth consent screen"** (left sidebar)
2. Select **"External"**
3. Click **"Create"**
4. Fill in:
   - **App name:** `Project Veritas`
   - **User support email:** Your email
   - **Developer contact email:** Your email
5. Click **"Save and Continue"**
6. **Scopes page:** Click **"Add or Remove Scopes"**
   - Check: `userinfo.email`
   - Check: `userinfo.profile`
   - Check: `openid`
7. Click **"Update"** → **"Save and Continue"**
8. **Test users page:** Skip (click **"Save and Continue"**)
9. **Summary page:** Click **"Back to Dashboard"**

### Step 5: Create OAuth Credentials
1. Go to: **"APIs & Services"** → **"Credentials"** (left sidebar)
2. Click **"+ Create Credentials"** (top)
3. Select **"OAuth client ID"**
4. Application type: **"Web application"**
5. Name: `Project Veritas Web Client`

6. **Authorized JavaScript origins:**
   Click **"+ Add URI"** and add:
   ```
   https://project-veritas.streamlit.app
   ```
   Click **"+ Add URI"** again:
   ```
   https://projectveritas.app
   ```
   Click **"+ Add URI"** again:
   ```
   http://localhost:8501
   ```

7. **Authorized redirect URIs:**
   Click **"+ Add URI"** and add:
   ```
   https://project-veritas.streamlit.app
   ```
   Click **"+ Add URI"** again:
   ```
   https://projectveritas.app
   ```
   Click **"+ Add URI"** again:
   ```
   http://localhost:8501
   ```

8. Click **"Create"**

### Step 6: Copy Your Credentials
A popup appears with:
- **Client ID** - looks like: `123456789-abc123xyz.apps.googleusercontent.com`
- **Client secret** - looks like: `GOCSPX-abc123xyz789`

**Copy both! You'll need them in the next step.**

---

## Step 7: Update Streamlit Secrets

1. Go to your Streamlit app dashboard
2. Click **Settings** → **Secrets**
3. **Replace with this** (use YOUR credentials from Step 6):

```toml
OPENAI_API_KEY = "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"

GOOGLE_CLIENT_ID = "PASTE_YOUR_CLIENT_ID_HERE"

GOOGLE_CLIENT_SECRET = "PASTE_YOUR_CLIENT_SECRET_HERE"

ALLOWED_EMAILS = "tyler@apexacceleration.com"

redirect_uri = "https://project-veritas.streamlit.app"
```

4. Click **"Save"**
5. Wait 30 seconds for redeploy

---

## Step 8: Test

1. Visit: `https://project-veritas.streamlit.app`
2. You should see: **"🔐 Sign In Required"**
3. Click **"🔑 Sign in with Google"**
4. Sign in with: `tyler@apexacceleration.com`
5. You should see: **"✅ Welcome, tyler@apexacceleration.com!"**
6. ✅ **Done!**

---

## Troubleshooting

### Still getting "invalid_grant"?
- **Check:** Client ID ends with `.apps.googleusercontent.com`
- **Check:** Client Secret starts with `GOCSPX-`
- **Check:** No extra spaces in Streamlit secrets
- **Check:** Redirect URI in Google Console is exactly: `https://project-veritas.streamlit.app`

### "Error 400: redirect_uri_mismatch"?
- Go back to Google Cloud Console → Credentials
- Edit your OAuth client
- Make sure redirect URIs include: `https://project-veritas.streamlit.app`

### "Access blocked: This app hasn't been verified"?
- Click **"Advanced"** → **"Go to Project Veritas (unsafe)"**
- This is normal for apps with <100 users
- To remove this warning, you'd need to go through Google's verification process (not necessary for family use)

---

## What Credentials Look Like

**Client ID example:**
```
123456789012-abc123def456ghi789jkl012mno345pq.apps.googleusercontent.com
```

**Client Secret example:**
```
GOCSPX-1a2b3c4d5e6f7g8h9i0j
```

**If yours don't look like this, you may have copied the wrong thing!**

---

## Need Help?

If you're stuck at any step, the issue is likely:
1. Haven't created OAuth credentials yet → Do Step 5
2. Copied wrong credentials → Check they match the format above
3. Redirect URI mismatch → Check Step 5, item 7

---

**Once this is done, your app will be fully protected with Google OAuth email whitelisting! 🔒**
