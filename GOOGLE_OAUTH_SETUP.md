# 🔐 Google OAuth Setup Guide

This guide walks you through setting up Google OAuth for Project Veritas so only your whitelisted family members can access the app.

---

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `Project Veritas`
4. Click **"Create"**

---

## Step 2: Enable Google+ API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for: `Google+ API`
3. Click on it and press **"Enable"**

---

## Step 3: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (allows anyone with a Google account to attempt login)
3. Click **"Create"**

4. Fill in the required fields:
   - **App name:** `Project Veritas`
   - **User support email:** Your email
   - **Developer contact email:** Your email
5. Click **"Save and Continue"**

6. **Scopes:** Click **"Add or Remove Scopes"**
   - Check: `userinfo.email`
   - Check: `userinfo.profile`
   - Check: `openid`
7. Click **"Save and Continue"**

8. **Test users:** (Optional for now)
   - You can add test users here, or skip
9. Click **"Save and Continue"**

---

## Step 4: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Application type: **"Web application"**
4. Name: `Project Veritas Web Client`

5. **Authorized JavaScript origins:**
   - Add: `https://projectveritas.app`
   - Add: `http://localhost:8501` (for local testing)

6. **Authorized redirect URIs:**
   - Add: `https://projectveritas.app`
   - Add: `http://localhost:8501` (for local testing)

7. Click **"Create"**

8. **IMPORTANT:** Copy both:
   - **Client ID** (looks like: `123456789.apps.googleusercontent.com`)
   - **Client Secret** (looks like: `GOCSPX-abc123xyz`)

---

## Step 5: Update Your `.env` File

Open your `.env` file and update these lines:

```env
# Replace with your actual credentials from Step 4
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123xyz

# Add your family's email addresses (comma-separated, no spaces after commas)
ALLOWED_EMAILS=tyler@apexacceleration.com,mom@gmail.com,dad@gmail.com,sister@gmail.com
```

**⚠️ Security Note:**
- Never commit `.env` to GitHub (it's already in `.gitignore`)
- Keep your `GOOGLE_CLIENT_SECRET` private

---

## Step 6: Add Environment Variables to Deployment Platform

### For Streamlit Community Cloud:

1. Go to your app settings
2. Click **"Secrets"**
3. Add the following secrets:
```toml
OPENAI_API_KEY = "sk-proj-..."
GOOGLE_CLIENT_ID = "123456789.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-abc123xyz"
ALLOWED_EMAILS = "tyler@apexacceleration.com,family@gmail.com"
```

### For Vercel (not recommended for Streamlit):

Vercel doesn't natively support Streamlit. Use Streamlit Community Cloud instead.

### For Railway/Render/DigitalOcean:

Add environment variables in their respective dashboards with the same names as in `.env`.

---

## Step 7: How to Add/Remove Family Members

To add or remove people who can access the app:

1. Open `.env` file
2. Update `ALLOWED_EMAILS` line:
```env
ALLOWED_EMAILS=email1@gmail.com,email2@gmail.com,email3@gmail.com
```
3. Update the same variable in your deployment platform's environment variables
4. Redeploy the app

**Important:**
- Use lowercase emails
- No spaces after commas
- Users must sign in with the exact email address listed

---

## Step 8: Test Authentication

1. Start your app locally:
```bash
streamlit run app.py
```

2. Visit `http://localhost:8501`
3. You should see a "Sign In Required" page
4. Click the Google sign-in button
5. Sign in with a whitelisted email
6. You should see "✅ Welcome, your-email@gmail.com!"

---

## Troubleshooting

### "Error 400: redirect_uri_mismatch"
- Make sure you added your app's URL to **Authorized redirect URIs** in Google Cloud Console
- URL must match exactly (including https://)

### "Access denied. Your email is not authorized"
- Check that your email is in the `ALLOWED_EMAILS` list
- Make sure there are no extra spaces in the `.env` file
- Emails are case-sensitive (use lowercase)

### "Google OAuth not configured"
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in `.env`
- Restart your Streamlit app after updating `.env`

### OAuth library not installed
```bash
pip install -r requirements.txt
```

---

## What Your Family Will See

**Unauthenticated users:**
- See "Sign In Required" screen
- Click "Sign in with Google" button
- Redirected to Google login
- If email is whitelisted → Access granted
- If email is NOT whitelisted → "Access denied" message

**Authenticated users:**
- See full Project Veritas interface
- Can analyze reviews
- See "Sign Out" button in top-right corner

---

## Security Features

✅ **Only whitelisted emails can access** - Even if someone finds your URL, they can't use it without being on your list

✅ **Google handles authentication** - No passwords to manage, no database needed

✅ **Session-based** - Users stay logged in during their session

✅ **Sign out option** - Users can manually sign out

✅ **API key protection** - Your OpenAI API key is never exposed to users

---

## Next Steps

Once OAuth is working:
1. ✅ Test locally with your email
2. ✅ Add your family's emails to `ALLOWED_EMAILS`
3. ✅ Deploy to Streamlit Community Cloud (see DEPLOY_STREAMLIT.md)
4. ✅ Update Google OAuth redirect URI with production URL
5. ✅ Share the URL with your family - they can sign in with their Google accounts!

---

**Questions?** Check the [Troubleshooting](#troubleshooting) section above or review Google's [OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2).
