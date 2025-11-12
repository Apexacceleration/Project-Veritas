# ⚡ Quick Deploy Guide - 20 Minutes to Live

**Get Project Veritas online with Google OAuth protection in ~20 minutes**

---

## Why Vercel Failed

The 404 error you got was because:
- ❌ Vercel doesn't natively support Streamlit apps
- ❌ Docker support on Vercel is limited
- ❌ Streamlit needs persistent WebSocket connections

**Solution:** Use Streamlit Community Cloud instead (FREE, built for Streamlit)

---

## Step-by-Step Deploy (20 minutes)

### Part 1: Google OAuth Setup (10 minutes)

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create Project:**
   - Click "Select a project" → "New Project"
   - Name: `Project Veritas`
   - Click "Create"

3. **Enable Google+ API:**
   - Go to "APIs & Services" → "Library"
   - Search: `Google+ API`
   - Click "Enable"

4. **Configure OAuth Consent:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Select "External"
   - Fill in:
     - App name: `Project Veritas`
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue" (3 times)

5. **Create Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Type: "Web application"
   - Name: `Project Veritas Web`
   - Add JavaScript origins:
     - `https://project-veritas.streamlit.app`
     - `http://localhost:8501`
   - Add Redirect URIs:
     - `https://project-veritas.streamlit.app`
     - `http://localhost:8501`
   - Click "Create"

6. **Copy Credentials:**
   - Copy `Client ID` (looks like: `123456.apps.googleusercontent.com`)
   - Copy `Client Secret` (looks like: `GOCSPX-abc123`)
   - Keep these safe for next part!

---

### Part 2: Deploy to Streamlit Cloud (10 minutes)

1. **Sign up:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "Continue with GitHub"
   - Authorize Streamlit

2. **Deploy App:**
   - Click "New app"
   - Repository: `Apexacceleration/Project-Veritas`
   - Branch: `main`
   - Main file: `app.py`
   - App URL: `project-veritas` (becomes: project-veritas.streamlit.app)
   - Click "Deploy!"

3. **Wait 2-5 minutes** (installing dependencies)

4. **Add Secrets:**
   - Click "⚙️ Settings" → "Secrets"
   - Paste this (replace with YOUR values):
   ```toml
   OPENAI_API_KEY = "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"

   GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"

   GOOGLE_CLIENT_SECRET = "GOCSPX-YOUR_SECRET_HERE"

   ALLOWED_EMAILS = "tyler@apexacceleration.com,family@gmail.com"
   ```
   - Click "Save"
   - App redeploys automatically (wait 1 minute)

5. **Test:**
   - Visit: `https://project-veritas.streamlit.app`
   - You should see "Sign In Required"
   - Click "Sign in with Google"
   - Sign in with your email (must be in ALLOWED_EMAILS)
   - ✅ Success! You should see the app

---

### Part 3: Connect Custom Domain (Optional, 10 minutes)

1. **In Streamlit Cloud:**
   - Go to app settings → "Custom domain"
   - Enter: `projectveritas.app`
   - Copy the DNS records shown

2. **In Your Domain Registrar:**
   - Go to where you bought `projectveritas.app`
   - Add DNS records:
     ```
     Type: CNAME
     Host: @
     Value: [value from Streamlit]
     TTL: 3600

     Type: CNAME
     Host: www
     Value: [value from Streamlit]
     TTL: 3600
     ```

3. **Wait 5-60 minutes** for DNS propagation

4. **Update Google OAuth:**
   - Go back to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Edit your OAuth client
   - Add to JavaScript origins: `https://projectveritas.app`
   - Add to Redirect URIs: `https://projectveritas.app`
   - Click "Save"

5. **Test:**
   - Visit: `https://projectveritas.app`
   - Sign in with Google
   - ✅ Done!

---

## Quick Troubleshooting

### "streamlit-google-oauth library not installed"
- Check that `requirements.txt` includes it (it should)
- Try redeploying: Streamlit dashboard → "⋮" → "Reboot"

### "Google OAuth not configured"
- Make sure you added `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to Streamlit secrets
- Check for typos
- Make sure there are no extra spaces

### "No users are whitelisted"
- Add `ALLOWED_EMAILS` to Streamlit secrets
- Format: `email1@gmail.com,email2@gmail.com` (no spaces)

### "Error 400: redirect_uri_mismatch"
- Your deployed URL doesn't match what's in Google Cloud Console
- Add your exact URL to "Authorized redirect URIs"

### "Access denied" for whitelisted user
- Check email spelling in `ALLOWED_EMAILS`
- Use lowercase
- No spaces after commas
- User must sign in with exact email

---

## 📍 You Are Here

✅ Code is complete and pushed to GitHub
✅ Authentication is implemented
✅ Documentation is ready

**Next:** Follow the 3 parts above to deploy!

**Your repo:** https://github.com/Apexacceleration/Project-Veritas

---

## Add Family Members Later

1. Go to Streamlit app settings → "Secrets"
2. Update `ALLOWED_EMAILS`:
   ```toml
   ALLOWED_EMAILS = "tyler@apexacceleration.com,mom@gmail.com,dad@gmail.com"
   ```
3. Click "Save"
4. Share URL with them: `https://projectveritas.app`

They just click "Sign in with Google" and they're in!

---

## Cost

- Streamlit Cloud: **FREE** ✅
- Google OAuth: **FREE** ✅
- Domain: **$12/year** (already own)
- OpenAI API: **~$0.0015/analysis** (limits already set)

---

## Need More Help?

- **Full deployment guide:** [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)
- **OAuth setup guide:** [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)
- **Authentication summary:** [AUTHENTICATION_SUMMARY.md](AUTHENTICATION_SUMMARY.md)

---

**🎉 You're 20 minutes away from having a secure, family-friendly review analysis tool online!**
