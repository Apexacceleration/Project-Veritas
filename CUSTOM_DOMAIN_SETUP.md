# 🌐 Custom Domain Setup: projectveritas.app

**Goal:** Access your app at `projectveritas.app` instead of `username.streamlit.app`

---

## 📋 Overview

To use `projectveritas.app`, you need:

1. ✅ **Register the domain** (projectveritas.app)
2. ✅ **Deploy your app** (hosting platform)
3. ✅ **Configure DNS** (point domain to your app)
4. ✅ **Set up SSL** (HTTPS certificate)

**Total Cost:** $12-15/year (domain) + $0-7/month (hosting)

---

## 🎯 Recommended Approach

### Option 1: Streamlit Cloud + Custom Domain (EASIEST)

**Best for:** Family use, zero maintenance

**Steps:**
1. Register `projectveritas.app` ($12/year)
2. Deploy to Streamlit Cloud (free)
3. Point DNS to Streamlit (CNAME record)
4. Configure custom domain in Streamlit

**Pros:**
- ✅ Free hosting
- ✅ Zero maintenance
- ✅ Auto-scaling
- ✅ HTTPS included
- ✅ Simple setup

**Cons:**
- ⚠️ Requires Streamlit Teams plan ($250/month for custom domains)
- ⚠️ Alternative: Use subdomain on your own domain

**Cost:** $12/year (domain only) + $250/month (Streamlit Teams) = **TOO EXPENSIVE**

**Verdict:** ❌ Not cost-effective for family use

---

### Option 2: Vercel + Custom Domain (RECOMMENDED) ⭐

**Best for:** Professional setup, affordable, fast

**Steps:**
1. Register `projectveritas.app` ($12/year)
2. Deploy to Vercel (free tier available)
3. Connect custom domain (one-click)
4. Auto HTTPS (Let's Encrypt)

**Pros:**
- ✅ Free hosting (Vercel Hobby tier)
- ✅ Custom domain included (FREE)
- ✅ Automatic HTTPS
- ✅ Fast CDN
- ✅ Easy deployment
- ✅ Works with Streamlit (via Docker)

**Cons:**
- ⚠️ Requires converting Streamlit to Docker container
- ⚠️ Slight learning curve

**Cost:** $12/year (domain only) = **AFFORDABLE** ✅

**Verdict:** ⭐ **BEST OPTION**

---

### Option 3: DigitalOcean Droplet + Custom Domain

**Best for:** Full control, learning experience

**Steps:**
1. Register `projectveritas.app` ($12/year)
2. Rent DigitalOcean droplet ($4-6/month)
3. Deploy Streamlit on server
4. Configure DNS
5. Set up HTTPS (Let's Encrypt)

**Pros:**
- ✅ Full control
- ✅ Can run anything
- ✅ Affordable

**Cons:**
- ⚠️ Requires server management
- ⚠️ You maintain security updates
- ⚠️ More technical

**Cost:** $12/year + $6/month = **$84/year**

**Verdict:** ⭐⭐ Good option if you want to learn

---

### Option 4: Railway.app + Custom Domain

**Best for:** Simple deployment, pay-as-you-go

**Steps:**
1. Register `projectveritas.app` ($12/year)
2. Deploy to Railway (pay-as-you-go)
3. Connect custom domain (free on Pro plan)
4. Auto HTTPS

**Pros:**
- ✅ Easy deployment
- ✅ Custom domain on Pro plan ($20/month)
- ✅ Pay only for usage
- ✅ Native Streamlit support

**Cons:**
- ⚠️ $20/month for custom domain support

**Cost:** $12/year + $20/month = **$252/year**

**Verdict:** ⭐ Okay but expensive

---

## 🏆 RECOMMENDED: Vercel Setup (Step-by-Step)

### Phase 1: Register Domain

**Step 1: Check Domain Availability**

Go to: [namecheap.com](https://www.namecheap.com) or [porkbun.com](https://porkbun.com)

Search: `projectveritas.app`

**Expected Cost:**
- Namecheap: ~$12/year
- Porkbun: ~$8/year (cheaper!)
- Google Domains: ~$12/year

**Recommendation:** Use **Porkbun** (cheapest, good reputation)

**Step 2: Purchase Domain**

1. Add to cart
2. Enable "Auto-Renew" (so you don't lose it)
3. Disable "WhoisGuard" (optional privacy - not needed)
4. Pay with credit card

**You now own:** `projectveritas.app` ✅

---

### Phase 2: Prepare App for Vercel

**Step 1: Convert Streamlit to Docker**

I'll create the necessary files for you:

**File 1: `Dockerfile`**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**File 2: `vercel.json`**
```json
{
  "builds": [
    {
      "src": "Dockerfile",
      "use": "@vercel/docker"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}
```

**Step 2: Push to GitHub**

```bash
cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"

# Add Dockerfile and vercel.json
git add Dockerfile vercel.json
git commit -m "Add Vercel deployment config"
git push origin main
```

---

### Phase 3: Deploy to Vercel

**Step 1: Sign Up for Vercel**

1. Go to: [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

**Step 2: Import Project**

1. Click "Add New" → "Project"
2. Select your GitHub repo: `project-veritas`
3. Click "Import"
4. Configure:
   - Framework Preset: **Other**
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

**Step 3: Add Environment Variables**

In Vercel project settings:

1. Go to "Settings" → "Environment Variables"
2. Add:
   ```
   Name: OPENAI_API_KEY
   Value: sk-proj-your-actual-key-here
   Environment: Production
   ```
3. Click "Save"

**Step 4: Deploy**

Click "Deploy" button

Wait 2-3 minutes...

**You'll get:** `https://project-veritas-xyz.vercel.app`

---

### Phase 4: Connect Custom Domain

**Step 1: Add Domain in Vercel**

1. In Vercel project, go to "Settings" → "Domains"
2. Click "Add Domain"
3. Enter: `projectveritas.app`
4. Click "Add"

**Step 2: Configure DNS (in Porkbun/Namecheap)**

Vercel will show you DNS records to add:

**Add these records in your domain registrar:**

```
Type: A
Name: @
Value: 76.76.21.21
TTL: 600
```

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600
```

**Step 3: Wait for DNS Propagation**

- Takes 5 minutes to 24 hours (usually ~30 minutes)
- Vercel will auto-configure HTTPS (Let's Encrypt)

**Step 4: Test**

After DNS propagates, visit:
- `https://projectveritas.app` ✅
- `https://www.projectveritas.app` ✅

**Both work automatically!**

---

## 🔐 Security with Custom Domain

### SSL/HTTPS: Automatic ✅

Vercel provides:
- Free SSL certificate (Let's Encrypt)
- Auto-renewal (never expires)
- Forced HTTPS (HTTP → HTTPS redirect)

### Access Control

**By default:** Anyone with URL can access

**To add password protection:** I can modify `app.py` to add simple password

**Example:**
```python
# Family password: "veritas2025"
if not check_password():
    st.stop()
```

**Want me to add this?**

---

## 💰 Total Cost Breakdown

### Recommended Setup (Vercel):

| Item | Cost | Frequency |
|------|------|-----------|
| Domain (Porkbun) | $8 | Annual |
| Vercel Hosting | $0 | Free (Hobby tier) |
| SSL Certificate | $0 | Included |
| OpenAI API | $0.15-0.50 | Monthly |
| **TOTAL Year 1** | **$8 + ~$5** | **~$13/year** |

**Monthly equivalent:** ~$1.08/month

**VERY AFFORDABLE!** ✅

---

## 📊 Comparison Table

| Option | Domain | Hosting | SSL | Setup | Total/Year |
|--------|--------|---------|-----|-------|------------|
| **Vercel** ⭐ | $8 | $0 | Free | Easy | **$8** |
| Streamlit Teams | $12 | $3000 | Free | Easy | $3012 |
| DigitalOcean | $12 | $72 | Free | Medium | $84 |
| Railway Pro | $12 | $240 | Free | Easy | $252 |

**Winner:** Vercel (by far!) ⭐

---

## 🚀 Quick Start (Recommended Path)

### Today:

1. **Register domain** at [porkbun.com](https://porkbun.com)
   - Search: `projectveritas.app`
   - Purchase: ~$8
   - Time: 5 minutes

2. **I'll create deployment files for you**
   - Dockerfile
   - vercel.json
   - Time: 2 minutes

3. **Deploy to Vercel**
   - Sign up with GitHub
   - Import project
   - Add API key as env variable
   - Time: 10 minutes

4. **Connect domain**
   - Add domain in Vercel
   - Configure DNS in Porkbun
   - Wait 30 minutes for propagation

**Total time:** ~1 hour
**Total cost:** $8 (domain)

---

## 🎯 Alternative: Quick Test First

**Not ready to buy domain yet?**

**Option A: Use Vercel's free domain first**
- Deploy to Vercel
- Get: `https://project-veritas-xyz.vercel.app`
- Test everything works
- Add custom domain later (takes 5 mins)

**Option B: Use Streamlit Cloud (easiest)**
- Deploy to Streamlit Cloud
- Get: `https://username-project-veritas.streamlit.app`
- Share with family
- Upgrade to custom domain later (when you outgrow it)

---

## ❓ FAQ

**Q: Do I need to buy the domain before deploying?**
A: No! Deploy first, add domain later.

**Q: Will my app work during DNS propagation?**
A: Yes! Use Vercel's URL until DNS is ready.

**Q: Can I use a different domain name?**
A: Yes! Any domain works (e.g., `reviewchecker.app`, `fakereviews.com`)

**Q: What if projectveritas.app is taken?**
A: Try:
- `projectveritas.co`
- `veritasreviews.app`
- `reviewveritas.com`
- `getveritas.app`

**Q: Can I transfer my domain later?**
A: Yes! Domains can be transferred between registrars.

**Q: Will this work for my family?**
A: Yes! They access `projectveritas.app` just like any website.

**Q: What about email (e.g., team@projectveritas.app)?**
A: Not included, but can add for ~$1/month extra (Porkbun email forwarding).

---

## 🎉 What You Get

**With `projectveritas.app`:**

✅ Professional URL (easy to remember)
✅ HTTPS (secure, trust badge in browser)
✅ Fast loading (Vercel CDN)
✅ Mobile-friendly (works on any device)
✅ Always online (99.9% uptime)
✅ Family can bookmark it
✅ Looks legit (not .streamlit.app)

**Perfect for sharing with family!**

---

## 🚦 Next Steps

**Ready to proceed?**

1. **Want me to create the Dockerfile and vercel.json?** (2 mins)
2. **Should I add password protection to the app?** (5 mins)
3. **Need help buying the domain?** (I'll guide you)

**Or test first:**
- Deploy to Streamlit Cloud now (free)
- Add custom domain later (when ready)

**What would you like to do?** 🚀

---

**Last Updated:** 2025-11-12
