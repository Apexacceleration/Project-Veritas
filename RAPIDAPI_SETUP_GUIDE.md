# RapidAPI Multi-Account Setup Guide

**Goal:** Set up 5-10 RapidAPI accounts to aggregate free tiers (250-500+ requests/month)

---

## Why Multiple Accounts?

Each RapidAPI account gets its own free tier:
- Real-Time Amazon Data (OpenWeb Ninja): **100 requests/month FREE**
- Realtime Amazon Data (API World): **25 requests/month FREE**
- Scout Amazon Data: **50 requests/month FREE**

**Strategy:** Create 5+ accounts → Subscribe to different APIs → Get 250-500+ free requests total

---

## Step 1: Create Multiple RapidAPI Accounts (20 minutes)

### Use Gmail Plus Addressing

Gmail treats `yourname+anything@gmail.com` as the same inbox as `yourname@gmail.com`

**Create 5 accounts:**
1. tyler+api1@gmail.com
2. tyler+api2@gmail.com
3. tyler+api3@gmail.com
4. tyler+api4@gmail.com
5. tyler+api5@gmail.com

**All emails go to `tyler@gmail.com` inbox!**

### Account Creation Process

For each email address:

1. Go to [RapidAPI](https://rapidapi.com/)
2. Click "Sign Up"
3. Use one of your plus-addressed emails (tyler+api1@gmail.com)
4. Create password (can reuse same password for all)
5. Verify email (check tyler@gmail.com inbox)
6. Repeat for all 5 emails

---

## Step 2: Subscribe to Amazon APIs (10 minutes)

### Recommended Strategy: Mix Different APIs

Subscribe each account to a DIFFERENT API to maximize free tier diversity:

| Account | API to Subscribe | Free Tier | API Key Location |
|---------|-----------------|-----------|------------------|
| tyler+api1@gmail.com | Real-Time Amazon Data (OpenWeb Ninja) | 100 req/month | [Link](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data) |
| tyler+api2@gmail.com | Realtime Amazon Data (API World) | 25 req/month | [Link](https://rapidapi.com/apiworld/api/realtime-amazon-data) |
| tyler+api3@gmail.com | Scout Amazon Data | 50 req/month | [Link](https://rapidapi.com/scout-data/api/scout-amazon-data) |
| tyler+api4@gmail.com | Real-Time Amazon Data (repeat) | 100 req/month | Same as #1 |
| tyler+api5@gmail.com | Scout Amazon Data (repeat) | 50 req/month | Same as #3 |

**Total:** 325 requests/month FREE!

### For Each Account:

1. **Log into RapidAPI** with that account (tyler+api1@gmail.com)
2. **Go to the API link** from table above
3. **Click "Subscribe to Test"**
4. **Select "Basic" plan** ($0.00/mo)
5. **Confirm subscription**
6. **Copy your API key:**
   - Click "Code Snippets"
   - Look for `X-RapidAPI-Key: abc123...`
   - Copy the entire key
7. **Save key** in a text file for now

---

## Step 3: Add API Keys to Streamlit Secrets

Once you have all 5 API keys:

1. Go to [Streamlit Cloud Dashboard](https://share.streamlit.io)
2. Click your app → **⚙️ Settings** → **Secrets**
3. Add your keys (TOML format):

```toml
# Existing secrets (keep these)
OPENAI_API_KEY = "sk-proj-..."
ALLOWED_EMAILS = "tyler@apexacceleration.com"

# RapidAPI Keys (ADD THESE)
RAPIDAPI_KEY_1 = "your-first-api-key-here"
RAPIDAPI_KEY_2 = "your-second-api-key-here"
RAPIDAPI_KEY_3 = "your-third-api-key-here"
RAPIDAPI_KEY_4 = "your-fourth-api-key-here"
RAPIDAPI_KEY_5 = "your-fifth-api-key-here"
```

4. Click **Save**
5. App will automatically redeploy (wait 1 minute)

---

## Step 4: Test the Multi-API Rotation

1. Go to your deployed app: https://project-veritas.streamlit.app
2. Sign in with Google
3. Enter an Amazon product URL
4. Click "Analyze Reviews"
5. Watch the logs - you should see:
   ```
   🔑 Loaded 5 RapidAPI key(s)
   🚀 Trying API key #1...
      📡 Trying Real-Time Amazon Data (OpenWeb Ninja)...
   ✅ Success with API key #1 using Real-Time Amazon Data!
   ```

---

## How the Rotation Works

**Project Veritas automatically:**
1. Tries API key #1 with all 3 API services
2. If rate limited (429), tries API key #2
3. If rate limited, tries API key #3
4. Continues until finding a working key
5. If all keys exhausted, shows friendly error message

**You don't need to do anything!** The rotation is automatic.

---

## Monitoring Usage

### Check Your Current Usage:

1. Log into each RapidAPI account
2. Go to [My Apps](https://rapidapi.com/developer/apps)
3. Click your app
4. See "Requests this month" for each API

### When a Key Gets Rate Limited:

**Don't worry!** The system automatically tries the next key.

### Free Tier Resets:

All free tiers reset on the **1st of each month** at midnight UTC.

---

## Cost Analysis

### With 5 Free Accounts:
- **325 requests/month FREE**
- Each analysis uses ~3-5 requests
- **~65-100 product analyses per month FREE**

### If You Need More:

Create 5 more accounts (tyler+api6@gmail.com through tyler+api10@gmail.com):
- **650 requests/month FREE**
- **~130-200 product analyses per month FREE**

### If You STILL Need More:

Upgrade ONE account to paid tier:
- Real-Time Amazon Data: **$9.99/month** for 10,000 requests
- Much cheaper than other scraping services ($49+/month)

---

## Troubleshooting

### "No RapidAPI keys configured"
- You haven't added RAPIDAPI_KEY_1 to Streamlit secrets
- Add at least one key

### "All RapidAPI keys have reached their rate limits"
- All your accounts are exhausted for this month
- Wait until next month (resets on 1st)
- OR create more accounts
- OR upgrade one account to paid

### "API authentication failed" (403 error)
- API key is invalid or expired
- Check you copied the full key correctly
- Make sure you're subscribed to the API

### "Could not extract ASIN from URL"
- URL format is wrong
- Should be: `https://amazon.com/dp/B08N5WRWNW`
- OR: `https://amazon.com/product-name/dp/B08N5WRWNW`

---

## Quick Reference: API Links

- [Real-Time Amazon Data (OpenWeb Ninja)](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data) - 100 req/month
- [Realtime Amazon Data (API World)](https://rapidapi.com/apiworld/api/realtime-amazon-data) - 25 req/month
- [Scout Amazon Data](https://rapidapi.com/scout-data/api/scout-amazon-data) - 50 req/month

---

## Next Steps

**Right now, you have:**
- ✅ 1 RapidAPI account with 100 requests/month
- ✅ Multi-API rotation code deployed and ready
- ⏳ Need to create 4 more accounts

**To maximize your free tier:**
1. Create 4 more RapidAPI accounts (15 minutes)
2. Subscribe each to a different API (10 minutes)
3. Add all 5 API keys to Streamlit secrets (5 minutes)
4. **Total time: 30 minutes to get 325 free requests/month**

---

**Questions?** Check [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for other setup help.
