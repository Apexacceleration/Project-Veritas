# 🚀 Deploy Project Veritas to Streamlit Community Cloud

**Recommended Deployment Platform for Streamlit Apps**

Streamlit Community Cloud is **FREE**, officially supports Streamlit apps, and is much easier than Vercel for this use case.

---

## Why Streamlit Community Cloud?

✅ **Free** - No credit card required
✅ **Native Streamlit support** - Built specifically for Streamlit apps
✅ **Custom domains** - Connect projectveritas.app
✅ **Automatic deployments** - Deploys on every GitHub push
✅ **Environment variables** - Easy secret management
✅ **No Docker needed** - Just push your code

---

## Prerequisites

- [x] GitHub account (you have one)
- [x] Code pushed to GitHub repo: `https://github.com/Apexacceleration/Project-Veritas`
- [ ] Streamlit Community Cloud account (free)
- [ ] Google OAuth credentials (see GOOGLE_OAUTH_SETUP.md)

---

## Step 1: Create Streamlit Community Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Continue with GitHub"**
3. Authorize Streamlit to access your GitHub account
4. ✅ Done!

---

## Step 2: Deploy Your App

1. Click **"New app"**
2. Select your repository: `Apexacceleration/Project-Veritas`
3. Branch: `main`
4. Main file path: `app.py`
5. App URL (customize): `project-veritas` or `veritas-reviews`
   - Your app will be at: `https://project-veritas.streamlit.app`
6. Click **"Deploy!"**

**⏱️ First deployment takes 2-5 minutes** (installs dependencies)

---

## Step 3: Add Secret Environment Variables

1. In your app dashboard, click **"⚙️ Settings"** → **"Secrets"**
2. Add your secrets in TOML format:

```toml
# OpenAI API Key
OPENAI_API_KEY = "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"

# Google OAuth Credentials (get from: https://console.cloud.google.com)
GOOGLE_CLIENT_ID = "your-client-id-here.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-your-secret-here"

# Whitelisted Emails (comma-separated, no spaces after commas)
ALLOWED_EMAILS = "tyler@apexacceleration.com,family@gmail.com,friend@gmail.com"
```

3. Click **"Save"**
4. App will automatically redeploy with new secrets

---

## Step 4: Connect Your Custom Domain (projectveritas.app)

### Option A: Use Streamlit Subdomain (Easiest)

Your app is automatically available at:
```
https://project-veritas.streamlit.app
```

**✅ No DNS setup needed!** Share this URL with your family.

---

### Option B: Use Your Custom Domain (projectveritas.app)

1. In your app settings, go to **"Custom domain"**
2. Enter: `projectveritas.app`
3. Streamlit will show you DNS records to add

4. **Add DNS records in your domain registrar:**
   - Go to where you bought `projectveritas.app`
   - Add a `CNAME` record:
     ```
     Host: @
     Type: CNAME
     Value: [provided by Streamlit]
     TTL: 3600
     ```
   - Add a `CNAME` record for www:
     ```
     Host: www
     Type: CNAME
     Value: [provided by Streamlit]
     TTL: 3600
     ```

5. **Wait 5-60 minutes** for DNS propagation
6. ✅ Your app will be live at `https://projectveritas.app`!

---

## Step 5: Update Google OAuth Redirect URI

Once your app is deployed, update your Google Cloud Console:

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Edit your OAuth client
3. **Authorized JavaScript origins:**
   - Add: `https://project-veritas.streamlit.app` (or your custom domain)
4. **Authorized redirect URIs:**
   - Add: `https://project-veritas.streamlit.app` (or your custom domain)
5. Click **"Save"**

---

## Step 6: Test Your Deployed App

1. Visit your app URL: `https://project-veritas.streamlit.app`
2. You should see the **"Sign In Required"** page
3. Click **"Sign in with Google"**
4. Sign in with a whitelisted email
5. You should see: **"✅ Welcome, your-email@gmail.com!"**
6. Try analyzing an Amazon product!

---

## Step 7: Share with Your Family

Send them the URL:
```
https://projectveritas.app
```
or
```
https://project-veritas.streamlit.app
```

They'll need to:
1. Click "Sign in with Google"
2. Use an email address you added to `ALLOWED_EMAILS`
3. That's it! They can now use Project Veritas

---

## Automatic Updates

Every time you push to GitHub, your app automatically redeploys!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# ✅ Streamlit automatically redeploys in 1-2 minutes
```

---

## Managing Environment Variables

### To Add a New Family Member:

1. Go to app settings → **Secrets**
2. Update `ALLOWED_EMAILS`:
```toml
ALLOWED_EMAILS = "tyler@apexacceleration.com,newperson@gmail.com,anotherperson@gmail.com"
```
3. Click **"Save"**
4. App redeploys automatically

### To Change OpenAI API Key:

1. Go to app settings → **Secrets**
2. Update `OPENAI_API_KEY`
3. Click **"Save"**

---

## Monitoring Usage

### App Analytics:
- Go to your app dashboard
- See visitor count, CPU usage, memory usage
- Monitor uptime

### OpenAI API Usage:
- Go to [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- See daily/monthly costs
- Set spending limits if needed

---

## Troubleshooting

### "Oh no!" error page
- Check app logs: Click **"Manage app"** → **"Logs"**
- Common issues:
  - Missing environment variable
  - Syntax error in code
  - Missing dependency in requirements.txt

### Google OAuth not working
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in Secrets
- Verify redirect URI matches your deployed URL exactly
- See GOOGLE_OAUTH_SETUP.md for detailed troubleshooting

### "Module not found" error
- Check that dependency is in `requirements.txt`
- Redeploy app (forces reinstall of dependencies)

### App is slow
- First load is always slower (cold start)
- Subsequent loads are faster
- Consider upgrading to Streamlit Teams (paid) for better performance

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| **Streamlit Community Cloud** | FREE ✅ |
| **GitHub** | FREE ✅ |
| **Google OAuth** | FREE ✅ |
| **Domain (projectveritas.app)** | ~$12/year (you already own it) |
| **OpenAI API** | ~$0.0015 per analysis (GPT-5-mini) |

**Total cost for 100 analyses/month:** ~$0.15 + domain fee

**Your OpenAI limits protect you from runaway costs!**

---

## Alternative: Private Deployment

If you want to keep it completely private (no public URL):

1. In app settings → **"Sharing"**
2. Toggle **"Private"**
3. Only people you explicitly invite can access
4. They still need to be whitelisted in `ALLOWED_EMAILS`

---

## Next Steps

- [x] Deploy to Streamlit Community Cloud
- [x] Set up environment variables
- [ ] Set up Google OAuth (see GOOGLE_OAUTH_SETUP.md)
- [ ] Connect custom domain (optional)
- [ ] Add family emails to whitelist
- [ ] Test with all family members
- [ ] Share URL with family!

---

## Why Not Vercel?

Vercel is great for Next.js/React apps, but:
- ❌ Doesn't natively support Streamlit
- ❌ Requires complex Docker setup
- ❌ Limited serverless execution time (Streamlit needs persistent connection)
- ❌ More expensive for long-running apps

Streamlit Community Cloud is purpose-built for Streamlit apps.

---

**🎉 You're all set!** Your family can now use Project Veritas to analyze Amazon reviews safely and easily.
