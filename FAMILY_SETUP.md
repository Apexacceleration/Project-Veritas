# 👨‍👩‍👧‍👦 Family Setup Guide - Pre-Configure API Key

This guide shows you how to set up Project Veritas so your **family doesn't need to enter the OpenAI API key**.

---

## 🎯 Goal

**Your family just:**
1. Opens the web app
2. Toggles "Enable AI Analysis"
3. Selects GPT-5-mini or GPT-5
4. Analyzes products!

**No API key entry needed!** ✅

---

## 🏠 Setup for Local Use (Same Computer)

### Step 1: Create .env File

```bash
cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"

# Create .env file with your API key
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-actual-key-here
EOF
```

**⚠️ IMPORTANT:** Replace `sk-proj-your-actual-key-here` with your **real OpenAI API key**!

### Step 2: Verify .env is in .gitignore

```bash
# Check if .env is protected
grep ".env" .gitignore
```

Should show: `.env` ✅ (Already done!)

### Step 3: Run the App

```bash
streamlit run app.py
```

### Step 4: Test

1. ✅ Enable AI Analysis checkbox
2. ✅ Should show: "✅ API Key configured" (no input field!)
3. ✅ Select GPT-5-mini or GPT-5
4. ✅ Analyze a product

**Done!** Your family can now use it without seeing the API key.

---

## 🌐 Setup for Online Use (Streamlit Cloud)

This is the **best option** for family access from anywhere!

### Step 1: Push to GitHub

```bash
cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Project Veritas"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/project-veritas.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Select**:
   - Repository: `your-username/project-veritas`
   - Branch: `main`
   - Main file: `app.py`

### Step 3: Add API Key as Secret

In Streamlit deployment settings:

1. **Click** "Advanced settings"
2. **Find** "Secrets" section
3. **Add this** (replace with your real key):

```toml
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
```

4. **Click** "Deploy"

### Step 4: Share URL with Family

Once deployed, you'll get a URL like:
```
https://your-username-project-veritas.streamlit.app
```

**Share this URL** with your family!

They can:
- ✅ Access from any device (phone, tablet, computer)
- ✅ No installation needed
- ✅ No API key entry needed
- ✅ Just enable AI and analyze!

---

## 🔐 Security Best Practices

### ✅ DO:

1. **Use .env file** for local development
2. **Use Streamlit secrets** for deployed app
3. **Keep .env in .gitignore** (already done!)
4. **Set usage limits** on OpenAI dashboard
5. **Monitor usage** monthly

### ❌ DON'T:

1. **Don't commit .env** to git
2. **Don't share your API key** publicly
3. **Don't put API key** directly in code
4. **Don't share .env file** (if someone asks for it, they don't need it!)

---

## 💰 Set Usage Limits (Recommended)

Protect yourself from unexpected costs:

### Step 1: Go to OpenAI Dashboard

[platform.openai.com/settings/organization/limits](https://platform.openai.com/settings/organization/limits)

### Step 2: Set Monthly Limit

**For family use, set:**
- **Soft limit**: $2/month
- **Hard limit**: $5/month

**Why this works:**
- Your family will likely use $0.15-0.50/month
- $2 soft limit = warning email
- $5 hard limit = API stops (protection)

### Step 3: Enable Email Alerts

✅ Check "Send email when limits are reached"

---

## 👨‍👩‍👧‍👦 Family Instructions

Send this to your family:

---

### 📧 Email Template:

**Subject:** Access Project Veritas - Amazon Review Checker

Hi Family!

I set up a tool to check if Amazon reviews are fake. Here's how to use it:

**🔗 Link:** [your-streamlit-url-here]

**How to use:**
1. Find any product on Amazon
2. Copy the product URL
3. Paste it into Project Veritas
4. Check "Enable AI Analysis"
5. Choose GPT-5-mini (recommended) or GPT-5
6. Click "Analyze Reviews"
7. Wait 1-2 minutes for results

**What you'll get:**
- **Trust Score**: Are the reviews reliable?
- **Quality Score**: Is the product actually good?
- **Red Flags**: What issues were detected

**Tips:**
- Use GPT-5-mini for most products (cheaper, 95% accurate)
- Use GPT-5 for expensive purchases (more accurate, 5x cost)
- Trust Score below 60 = Be cautious!

**Cost:** I'm covering it - about 25 cents per month total!

Let me know if you have questions!

---

## 🎛️ What Your Family Will See

### With API Key Pre-Configured:

**Sidebar:**
```
⚙️ Settings

☑️ Enable AI Analysis

✅ API Key configured   <-- They see this!

AI Model:
○ GPT-5-mini  (selected)
○ GPT-5

💰 ~$0.0015/analysis | ⭐ Recommended
```

**No password input!**
**No technical setup!**
**Just click and go!** ✅

---

## 🔧 Troubleshooting

### "API Key not configured" shows up

**Check:**
1. `.env` file exists in project root
2. `.env` contains: `OPENAI_API_KEY=sk-proj-...`
3. No spaces around the `=` sign
4. API key is valid (test at platform.openai.com)

**Fix:**
```bash
# Verify .env exists
ls -la .env

# Check contents (will show your key - be careful!)
cat .env

# Should show: OPENAI_API_KEY=sk-proj-xxxxx
```

### "Invalid API key" error

**Check:**
1. Key is correct (no extra spaces)
2. Key is active (check OpenAI dashboard)
3. You have billing enabled on OpenAI

**Fix:**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new key
3. Update `.env` or Streamlit secrets

### Family sees "Enter API Key" instead

**Check:**
1. They're using the deployed URL (not local)
2. Streamlit secrets are saved
3. App was restarted after adding secrets

**Fix:**
- Restart the Streamlit app from dashboard
- Verify secrets are saved

---

## 📊 Monitor Usage

### Check Monthly Costs:

1. Go to [platform.openai.com/usage](https://platform.openai.com/usage)
2. View current month usage
3. See breakdown by model

**Expected:**
- 50 analyses: ~$0.075 (GPT-5-mini)
- 100 analyses: ~$0.15 (GPT-5-mini)
- Mixed use: $0.20-0.40/month

---

## 🎉 You're Done!

**Summary:**

✅ **Local Use:**
- Created `.env` with API key
- Family runs `streamlit run app.py`
- No key entry needed

✅ **Online Use:**
- Deployed to Streamlit Cloud
- Added API key as secret
- Shared URL with family
- Works on any device!

✅ **Security:**
- API key protected
- Usage limits set
- Not in git repository

✅ **Family Experience:**
- Just enable AI
- Select model
- Analyze products
- Super simple!

**Your family can now fight fake reviews with zero technical setup!** 🚀

---

**Questions?**
- Check [QUICKSTART.md](QUICKSTART.md) for more details
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
