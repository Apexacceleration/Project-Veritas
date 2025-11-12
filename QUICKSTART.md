# ⚡ Project Veritas - Quick Start Guide

## 🎯 What You Have Now

✅ **Complete review analysis tool** with 8 red flag detection algorithms
✅ **GPT-5 AI analysis** - Most advanced model (45% fewer errors!)
✅ **Beautiful web interface** for family access
✅ **Command-line tool** for advanced users
✅ **Dual scoring system**: Trust Score + Quality Score

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd "/Users/apexacceleration/My Drive (tyler@apexacceleration.com) (1)/Software Projects/Project Veritas"

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Set Up OpenAI API (Optional but Recommended)

1. Get API key: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Uses GPT-5-mini** - Most accurate AI for fake review detection!
**Cost**: ~$0.001-0.002 per analysis (super cheap!)

### 3. Run the Web App

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` 🎉

---

## 💻 Two Ways to Use

### A. Web Interface (Family-Friendly)

```bash
streamlit run app.py
```

**Features**:
- 🌐 Beautiful UI
- 📊 Visual score displays
- 🤖 Toggle AI analysis on/off
- 🎛️ **Switch between GPT-5-mini and GPT-5** (NEW!)
- 💰 Live cost comparison for each model
- 📥 Download JSON reports
- 📱 Mobile-friendly

### B. Command Line (Power Users)

```bash
python src/main.py https://amazon.com/dp/B08N5WRWNW
```

**Features**:
- ⚡ Fast and direct
- 📄 JSON output
- 🔧 Scriptable
- 💾 Save reports with `-o report.json`

---

## 🌐 Deploy Online (For Family Access)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for full guide.

**Quick Deploy to Streamlit Cloud (FREE)**:

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app" → Select your repo → Deploy!

4. Add your `OPENAI_API_KEY` in Streamlit secrets

5. Share the URL with family! 🎉

**Total cost**: ~$0.50/month (just OpenAI API usage)

---

## 📊 Example Output

```json
{
  "project": "Project Veritas",
  "url": "https://amazon.com/dp/...",
  "trust_score": 68,
  "trust_grade": "C",
  "quality_score": 82,
  "quality_grade": "B",
  "total_reviews_analyzed": 250,
  "trusted_reviews_count": 127,
  "suspicious_reviews_count": 123,
  "red_flags_triggered": [
    "Review Velocity",
    "Generic Praise"
  ]
}
```

### What the Scores Mean:

**Trust Score** (Review Reliability):
- 🟢 **90-100 (A)**: Highly trustworthy reviews
- 🔵 **75-89 (B)**: Generally reliable
- 🟡 **60-74 (C)**: Mixed signals, proceed with caution
- 🟠 **45-59 (D)**: Significant red flags
- 🔴 **0-44 (F)**: High likelihood of manipulation

**Quality Score** (Actual Product Quality):
- Based on **trusted reviews only** after filtering fakes
- Same A-F scale
- Shows what real customers think

---

## 🎛️ Configuration

Edit [config.py](config.py) to adjust:

- **Penalty weights** for each red flag
- **Thresholds** for detection (e.g., what % is "suspicious")
- **OpenAI model** (default: gpt-4o-mini for cost efficiency)
- **Max reviews to scrape** (default: 500)

Example:
```python
# Make velocity detection stricter
VELOCITY_PENALTY = -20  # Was -15

# Require higher verified purchase %
VERIFIED_LOW_THRESHOLD = 0.60  # Was 0.50
```

---

## 🔍 How It Works

### Phase 1: Scraping
- Extracts reviews from Amazon product pages
- Anti-bot measures: rotating user agents, random delays
- Captures: text, rating, date, author, verified status, images

### Phase 2: Analysis (8 Red Flags)
1. ⏱️ Review Velocity Spike
2. 💬 Generic Praise Pattern
3. 👤 Suspicious Reviewer Profiles
4. 🔤 Linguistic Anomalies
5. 📊 Extreme Sentiment Imbalance
6. 📏 Review Length Extremes
7. ✅ Verified Purchase Ratio
8. 🔁 Repetitive Phrasing

### Phase 3: AI Enhancement (Optional)
- Uses OpenAI GPT-4o-mini
- Analyzes linguistic patterns
- Detects deceptive language
- Identifies coordinated campaigns

### Phase 4: Scoring
- **Trust Score**: Statistical + AI analysis of review dataset
- **Quality Score**: Sentiment analysis of trusted reviews only
- Converts to 0-100 scale + letter grades

---

## 📂 Project Structure

```
project-veritas/
├── app.py                    # 🌐 Streamlit web interface
├── config.py                 # ⚙️ All settings and thresholds
├── requirements.txt          # 📦 Dependencies
├── .env.example              # 🔐 Environment template
├── README.md                 # 📖 Full documentation
├── DEPLOYMENT.md             # 🚀 Deployment guide
├── QUICKSTART.md             # ⚡ This file
└── src/
    ├── main.py               # 🎯 Master orchestrator
    ├── scraper.py            # 🕷️ Amazon scraper
    ├── analyzer.py           # 🔍 8 red flag checks
    ├── ai_analyzer.py        # 🤖 OpenAI integration
    ├── scorer.py             # 📊 Trust + Quality scoring
    └── utils.py              # 🛠️ Helper functions
```

---

## 💡 Usage Tips

### For Best Results:
- ✅ **Enable AI analysis** for more accurate detection
- ✅ **Use products with 50+ reviews** for better statistical analysis
- ✅ **Check both scores**: Low Trust + High Quality = fake positive reviews
- ✅ **Read red flags**: They explain what was detected

### Limitations:
- ⚠️ Amazon may block scraping (use delays/proxies)
- ⚠️ No system is 100% accurate
- ⚠️ Small sample sizes (<20 reviews) are less reliable

---

## 🆘 Troubleshooting

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Amazon blocked my requests"**
- Increase delays in `config.py`
- Use proxies (see `.env.example`)

**"OpenAI API error"**
- Check API key in `.env`
- Verify you have credits: [platform.openai.com/usage](https://platform.openai.com/usage)

**"No reviews found"**
- Verify Amazon URL is correct
- Check if product has reviews

---

## 📚 Next Steps

1. **Test locally**: `streamlit run app.py`
2. **Try a few products**: See how scores vary
3. **Deploy online**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Share with family**: Send them the URL!
5. **Customize**: Adjust `config.py` to your preferences

---

## 💰 Costs Summary

| Service | Cost | Usage |
|---------|------|-------|
| Streamlit Cloud | $0/month | FREE tier (1 private app) |
| OpenAI API | ~$0.002/analysis | Only when AI enabled |
| Hosting | $0/month | Streamlit handles it |
| **Total** | **~$0.50/month** | Based on ~100 analyses |

---

## ✅ Ready to Go!

Everything is set up and ready. Just:

1. Install dependencies
2. Add OpenAI key (optional)
3. Run `streamlit run app.py`
4. Analyze your first product!

**Questions?** Check:
- [README.md](README.md) - Full documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy online
- [config.py](config.py) - All settings

---

**🎉 Happy truth-seeking!**

*"In vino veritas, in reviews... well, that's what we're here to find out."*
