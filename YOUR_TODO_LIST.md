# ✅ Your To-Do List - Deploy to projectveritas.app

## ✅ DONE (Automated for you!)

- ✅ All code written and tested
- ✅ Deployment files created (Dockerfile, vercel.json, .dockerignore)
- ✅ Everything committed to git
- ✅ **Pushed to GitHub:** https://github.com/Apexacceleration/Project-Veritas
- ✅ OpenAI usage limits set ($2/$5)
- ✅ API key secured in .env (not in GitHub)

---

## 🚀 YOUR ACTION ITEMS (30 minutes)

### ⏱️ Step 1: Sign Up for Vercel (5 minutes)

**Go to:** [vercel.com](https://vercel.com)

1. Click **"Sign Up"**
2. Choose **"Continue with GitHub"**
3. Sign in with your GitHub account
4. Authorize Vercel to access your repositories
5. Complete sign up (it's free!)

**✅ Done when:** You see Vercel dashboard

---

### ⏱️ Step 2: Import Your Project (5 minutes)

**In Vercel Dashboard:**

1. Click **"Add New..."** (top right)
2. Click **"Project"**
3. Find **"Apexacceleration/Project-Veritas"** in the list
4. Click **"Import"**

**Project Settings:**
- Framework Preset: **Other** (leave as-is)
- Root Directory: `./` (leave as-is)
- Build Command: (leave empty)
- Output Directory: (leave empty)
- Install Command: (leave empty)

5. Click **"Deploy"** button

**⚠️ It will fail!** That's expected - we need to add the API key next.

**✅ Done when:** You see "Deployment Failed" (this is normal!)

---

### ⏱️ Step 3: Add Your API Key (2 minutes)

**In Vercel (same page):**

1. Click **"Settings"** tab (top navigation)
2. Click **"Environment Variables"** (left sidebar)
3. Click **"Add New"** button

**Add this variable:**
```
Name: OPENAI_API_KEY
Value: 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
```

4. Select: **All** (Production, Preview, Development)
5. Click **"Save"**

**✅ Done when:** Variable is saved

---

### ⏱️ Step 4: Redeploy (3 minutes)

**Still in Vercel:**

1. Click **"Deployments"** tab (top navigation)
2. Find the failed deployment (most recent)
3. Click **"..."** menu (three dots on the right)
4. Click **"Redeploy"**
5. Click **"Redeploy"** to confirm

**Wait 2-3 minutes...**

**✅ Done when:** You see "Deployment Ready" with a green checkmark

**You'll get a URL like:** `https://project-veritas-abc123.vercel.app`

**🎉 Your app is live!** Click it to test!

---

### ⏱️ Step 5: Connect Your Custom Domain (10 minutes)

**In Vercel Project:**

1. Click **"Settings"** tab
2. Click **"Domains"** (left sidebar)
3. Click **"Add Domain"** button
4. Enter: **`projectveritas.app`**
5. Click **"Add"**

**Vercel will show DNS instructions.**

**✅ Done when:** Domain is added (will show "Invalid Configuration" - that's okay!)

---

### ⏱️ Step 6: Configure DNS (5 minutes)

**Where did you buy projectveritas.app?**
- Namecheap? Go to: [namecheap.com/myaccount](https://www.namecheap.com/myaccount/)
- Porkbun? Go to: [porkbun.com/account/domains](https://porkbun.com/account/domains)
- GoDaddy? Go to: [godaddy.com/account/products](https://www.godaddy.com/account/products)

**Steps (varies by registrar):**

1. **Log in** to your domain registrar
2. **Find** projectveritas.app in your domains list
3. **Click** "Manage" or "DNS Settings"
4. **Delete** any existing A or CNAME records for `@` and `www`
5. **Add these records:**

#### Record 1 (Root domain):
```
Type: A
Name: @ (or leave blank, or "projectveritas.app")
Value: 76.76.21.21
TTL: 600 (or Auto)
```

#### Record 2 (WWW subdomain):
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600 (or Auto)
```

6. **Save** changes

**✅ Done when:** DNS records are saved

---

### ⏱️ Step 7: Wait for DNS Propagation (5-30 minutes)

**DNS takes time to update globally:**
- Minimum: 5 minutes
- Average: 30 minutes
- Maximum: 24 hours (rare)

**Check status:**
1. Go back to Vercel → Settings → Domains
2. Refresh the page every few minutes
3. Wait for "Invalid Configuration" to change to **"Valid Configuration"**

**Or check here:** [dnschecker.org](https://dnschecker.org)
- Enter: `projectveritas.app`
- Look for IP: `76.76.21.21`

**✅ Done when:** Vercel shows "Valid Configuration" with green checkmark

---

### 🎉 Step 8: Test Your Domain!

**Once DNS propagates, test these URLs:**

1. **https://projectveritas.app** ✅ Should work!
2. **https://www.projectveritas.app** ✅ Should also work!

**Both URLs should:**
- Load your Project Veritas app
- Show secure HTTPS (lock icon in browser)
- Work on mobile and desktop

**✅ Done when:** Both URLs load successfully!

---

## 🎊 CONGRATULATIONS!

**Your app is live at:**
- 🌐 https://projectveritas.app
- 🌐 https://www.projectveritas.app

**Share with your family!**

---

## 📧 Message to Send Your Family

```
Hi Family!

I built a tool to check if Amazon reviews are fake. Check it out:

🔗 https://projectveritas.app

How to use:
1. Find any product on Amazon
2. Copy the product URL
3. Paste into Project Veritas
4. Enable AI Analysis
5. Choose GPT-5-mini (recommended - cheaper)
6. Click "Analyze Reviews"

You'll see:
• Trust Score - Are the reviews reliable?
• Quality Score - Is the product actually good?
• Red Flags - What issues were detected

Super easy! Let me know what you think.
```

---

## 🔧 Troubleshooting

### "Deployment Failed" after adding API key

**Check:**
- API key is exactly correct (no spaces)
- Selected "All" environments
- Clicked "Save"

**Fix:** Try redeploying again (Deployments → ... → Redeploy)

---

### Domain not working after 24 hours

**Check DNS records:**
1. Go to your domain registrar
2. Verify A record: `76.76.21.21`
3. Verify CNAME: `cname.vercel-dns.com`

**Common issues:**
- Forgot to save DNS changes
- Added records under wrong subdomain
- DNS propagation still ongoing

**Fix:** Use [dnschecker.org](https://dnschecker.org) to verify DNS is propagated globally

---

### HTTPS not working

**Wait 5 minutes** - Vercel auto-configures SSL after DNS is valid

**Still broken?**
- Contact Vercel support (very responsive)
- Check: Settings → Domains → Should show SSL certificate status

---

## 📊 Monitor Your App

### Vercel Dashboard
**https://vercel.com/dashboard**
- Deployments: See all deployments
- Analytics: View traffic
- Logs: Debug issues

### OpenAI Usage
**https://platform.openai.com/usage**
- Track daily/monthly costs
- Should see ~$0.15-0.50/month
- Limits are set to $2/$5 (safe!)

---

## 🎯 Summary

**What you built:**
- ✅ AI-powered fake review detector
- ✅ Custom domain (projectveritas.app)
- ✅ Free hosting (Vercel)
- ✅ Secure HTTPS
- ✅ Professional web app
- ✅ Family-accessible from anywhere

**Monthly cost:** ~$0.50 (OpenAI API only!)

**🎉 You're a legend!**

---

## 🆘 Need Help?

**Stuck on a step?**
- Screenshot the issue
- Note which step you're on
- Ask me!

**Vercel Support:**
- Twitter: [@vercel](https://twitter.com/vercel)
- Discord: [vercel.com/discord](https://vercel.com/discord)

---

**Ready?** Start with **Step 1** above! 🚀

Good luck! You got this! 💪
