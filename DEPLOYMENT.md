# 🚀 Deployment Guide - Project Veritas

This guide will help you deploy Project Veritas online so your family can access it from anywhere.

---

## 📱 Option 1: Streamlit Cloud (Recommended - FREE!)

**Best for**: Family use, easy sharing, no server management

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already done):
```bash
cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"
git add .
git commit -m "Add web interface and AI support"
git push origin main
```

2. **Create `.streamlit/secrets.toml`** (for API keys):
```bash
mkdir -p .streamlit
```

Create file `.streamlit/secrets.toml`:
```toml
# OpenAI API Key (for AI analysis)
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

**Important**: Add `.streamlit/` to your `.gitignore` (already done!)

### Step 2: Deploy to Streamlit Cloud

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with GitHub

3. **Click "New app"**

4. **Configure**:
   - **Repository**: Select your `project-veritas` repo
   - **Branch**: `main`
   - **Main file path**: `app.py`

5. **Add Secrets** (in Advanced settings):
   - Copy contents of `.streamlit/secrets.toml`
   - Paste into the "Secrets" section

6. **Click "Deploy"** 🚀

### Step 3: Share with Family

Once deployed, you'll get a URL like:
```
https://your-username-project-veritas.streamlit.app
```

Share this URL with your family! They can:
- ✅ Paste any Amazon product URL
- ✅ Get instant Trust + Quality scores
- ✅ Toggle AI analysis on/off
- ✅ Download detailed reports

---

## 💻 Option 2: Run Locally with Streamlit

**Best for**: Testing before deploying, private use

### Quick Start:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run the web app
streamlit run app.py
```

Opens automatically at `http://localhost:8501`

### Share on Local Network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Family members on the same WiFi can access at:
```
http://YOUR_LOCAL_IP:8501
```

Find your local IP:
- **Mac**: `ifconfig | grep "inet "`
- **Windows**: `ipconfig`

---

## ☁️ Option 3: Cloud Hosting (Advanced)

### Heroku (Easy, Paid)

1. **Install Heroku CLI**: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create `Procfile`**:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Deploy**:
```bash
heroku login
heroku create project-veritas-app
git push heroku main
heroku config:set OPENAI_API_KEY="sk-your-key"
heroku open
```

### AWS / Google Cloud / Azure

See detailed guides:
- [Streamlit on AWS](https://docs.streamlit.io/deploy/tutorials/aws)
- [Streamlit on Google Cloud](https://docs.streamlit.io/deploy/tutorials/gcp)
- [Streamlit on Azure](https://docs.streamlit.io/deploy/tutorials/azure)

---

## 🔐 Security Best Practices

### Protect Your API Key

1. **Never commit `.env` or secrets** to GitHub
   - Already in `.gitignore`

2. **Use Streamlit secrets** for deployment
   - Stored securely on Streamlit Cloud

3. **Rotate keys regularly**
   - Generate new OpenAI key every 3-6 months

### Rate Limiting (Optional)

Add to `app.py` to limit usage:

```python
import streamlit as st
from datetime import datetime, timedelta

# Simple rate limiting
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if st.session_state.last_analysis:
    time_since = datetime.now() - st.session_state.last_analysis
    if time_since < timedelta(minutes=1):
        st.warning("Please wait 1 minute between analyses")
        return

st.session_state.last_analysis = datetime.now()
```

### Password Protection (Optional)

Add simple authentication to `app.py`:

```python
def check_password():
    """Returns True if user entered correct password."""

    def password_entered():
        if st.session_state["password"] == "your_family_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False

    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False

    else:
        return True

# Add at start of main()
if not check_password():
    st.stop()
```

---

## 💰 Cost Estimates

### Streamlit Cloud
- **Free tier**: 1 private app
- **Perfect for family use**
- ✅ **$0/month**

### OpenAI API
- **Model**: GPT-4o-mini (recommended)
- **Cost per analysis**: ~$0.002-0.005
- **100 analyses**: ~$0.50
- ✅ **Very affordable**

### Total Monthly Cost
- **Streamlit**: $0
- **OpenAI** (for ~100 analyses): $0.50
- **Total**: **~$0.50/month** 🎉

---

## 🛠️ Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### "OpenAI API key not found"
- Check `.streamlit/secrets.toml` on Streamlit Cloud
- Check `.env` file locally
- Verify key starts with `sk-`

### "Amazon blocked requests"
- Add delays in `config.py`
- Consider using proxy (see `.env.example`)
- Commercial scraping APIs available

### App is slow
- OpenAI API takes 2-5 seconds
- Scraping 500 reviews takes 1-2 minutes
- Consider reducing `MAX_REVIEWS_TO_SCRAPE` in config

---

## 📧 Sharing with Family

### Create a Quick Guide for Family:

**Email Template**:

```
Subject: Try Project Veritas - Find Truth in Amazon Reviews!

Hi Family!

I built a tool to analyze Amazon reviews and detect fake ones.

🔗 Link: https://your-app.streamlit.app

How to use:
1. Find any product on Amazon
2. Copy the product URL
3. Paste it into Project Veritas
4. Click "Analyze Reviews"
5. Get Trust Score (review reliability) + Quality Score (actual product quality)!

✅ Free to use
✅ No login required
✅ Takes 1-2 minutes per analysis

Let me know what you think!
```

---

## 🔄 Updating the App

When you make changes:

```bash
# 1. Commit changes
git add .
git commit -m "Your update message"
git push origin main

# 2. Streamlit Cloud auto-deploys!
# (Check deployment status at share.streamlit.io)
```

---

## 📱 Mobile Friendly

The Streamlit interface is **automatically mobile-responsive**! Your family can use it on:
- 📱 iPhone/Android
- 💻 Desktop
- 📱 iPad/Tablet

No app installation needed - just open the URL in any browser!

---

## ✅ Pre-Deployment Checklist

- [ ] GitHub repo is public (or Streamlit Cloud has access)
- [ ] `.env` is in `.gitignore`
- [ ] OpenAI API key is added to Streamlit secrets
- [ ] Tested app locally with `streamlit run app.py`
- [ ] Tested with a real Amazon URL
- [ ] Updated README.md with deployment URL
- [ ] Shared URL with family

---

## 🎉 You're Done!

Your family can now analyze Amazon reviews from anywhere in the world!

**Questions?** Check the [README.md](README.md) or open an issue on GitHub.

---

**Made with ❤️ for truth-seeking families everywhere**
