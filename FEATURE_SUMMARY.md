# ✨ Project Veritas - Feature Summary

**Version 1.1.0** - Complete AI-Powered Review Analysis Tool

---

## 🎯 Core Features

### 1. 🔍 Dual Scoring System

**Trust Score (0-100)**
- Measures reliability of review dataset
- Detects fake, incentivized, and manipulated reviews
- Letter grades: A (90-100) to F (0-44)
- Based on 8 statistical + linguistic red flags

**Quality Score (0-100)**
- Measures actual product quality
- Uses only trusted reviews (filters out fakes)
- Independent from Trust Score
- Shows what real customers think

**Example:**
- Trust Score: 45 (F) = "Many fake reviews detected"
- Quality Score: 85 (B) = "But actual product is good!"

---

### 2. 🤖 AI-Powered Analysis (GPT-5)

**Model Selection Toggle** ⭐ NEW!
- Switch between GPT-5-mini and full GPT-5
- Live cost comparison displayed
- Easy radio button in web interface
- No code changes needed

**GPT-5-mini (Default - Recommended)**
- 95% of GPT-5's accuracy
- $0.0015 per analysis (~$0.15/month)
- 45% fewer hallucinations vs GPT-4o
- Perfect for personal/family use

**GPT-5 (Premium Option)**
- Maximum accuracy (100%)
- $0.0075 per analysis (~$0.75/month)
- Best for professional use
- Superior at edge cases

**AI Capabilities:**
- Linguistic deception detection
- Coordinated campaign identification
- Sentiment-rating coherence analysis
- Pattern recognition across reviews

---

### 3. 🚩 8 Red Flag Detectors

**Statistical Analysis:**
1. **Review Velocity Spike** - Unnatural bursts of reviews
2. **Extreme Sentiment Imbalance** - Suspicious rating distributions
3. **Verified Purchase Ratio** - Low verification percentage
4. **Review Length Extremes** - Too short or too long

**Linguistic Analysis:**
5. **Generic Praise Pattern** - Vague, non-specific language
6. **Linguistic Anomalies** - Keyword stuffing, poor grammar
7. **Repetitive Phrasing** - Identical phrases across reviews
8. **Suspicious Reviewer Profile** - Unusual reviewer patterns

**Each detector:**
- Applies penalties to Trust Score
- Marks suspicious reviews
- Provides detailed explanations
- Configurable thresholds in config.py

---

### 4. 🌐 Beautiful Web Interface (Streamlit)

**User Experience:**
- Clean, modern design
- Color-coded score displays
- Mobile-responsive
- Zero learning curve

**Sidebar Settings:**
- ✅ Toggle AI analysis on/off
- 🎛️ **Switch GPT-5-mini ↔ GPT-5** (NEW!)
- 🔑 Secure API key input
- 💰 Live cost display
- 📊 Model comparison table

**Results Display:**
- Visual score boxes (color-coded by grade)
- Summary metrics (total, trusted, suspicious)
- Red flag warnings with details
- AI insights section
- Download JSON reports

**Accessibility:**
- Works on desktop, tablet, mobile
- No login required
- Fast load times
- Intuitive navigation

---

### 5. 🛠️ Command-Line Interface

**For Power Users:**
```bash
# Basic analysis
python src/main.py https://amazon.com/dp/PRODUCT_ID

# Save report
python src/main.py URL --output report.json

# Quiet mode (JSON only)
python src/main.py URL --quiet
```

**Features:**
- Fast execution
- Scriptable (automation)
- CI/CD integration
- Batch processing ready

---

### 6. ⚙️ Highly Configurable

**All thresholds customizable in [config.py](config.py):**

```python
# Adjust penalties
VELOCITY_PENALTY = -15  # Change to -20 for stricter

# Adjust detection thresholds
VERIFIED_LOW_THRESHOLD = 0.50  # Change to 0.60

# Change AI model
OPENAI_MODEL = "gpt-5-mini"  # Or "gpt-5" or "gpt-5-nano"

# Scraping settings
MAX_REVIEWS_TO_SCRAPE = 500
REQUEST_MIN_DELAY = 2.0
```

**No code changes needed** - just edit config values!

---

### 7. 🕷️ Resilient Scraper

**Amazon Scraper Features:**
- Anti-bot measures (user agent rotation, delays)
- Error handling and retry logic
- Graceful degradation
- Extracts: text, rating, date, author, verified status, images

**Anti-Scraping Tactics:**
- Random delays (2-5 seconds)
- Rotating user agents (5 browsers)
- Request timeout handling
- CAPTCHA detection

**Optional Enhancements:**
- Proxy support (via .env)
- Commercial API integration ready
- Rate limiting built-in

---

### 8. 📊 Detailed JSON Reports

**Output Format:**
```json
{
  "project": "Project Veritas",
  "url": "...",
  "trust_score": 68,
  "trust_grade": "C",
  "trust_summary": "...",
  "quality_score": 82,
  "quality_grade": "B",
  "quality_summary": "...",
  "total_reviews_analyzed": 250,
  "trusted_reviews_count": 127,
  "suspicious_reviews_count": 123,
  "red_flags_triggered": [...],
  "ai_insights": {...}
}
```

**Download Options:**
- JSON (machine-readable)
- Timestamped filenames
- One-click download from web UI

---

### 9. 🚀 Easy Deployment

**Streamlit Cloud (FREE):**
- One-click deploy from GitHub
- Free hosting (1 private app)
- Automatic HTTPS
- Share URL with family

**Total Setup Time:** ~15 minutes

**See [DEPLOYMENT.md](DEPLOYMENT.md) for guide**

---

### 10. 📚 Comprehensive Documentation

**6 Documentation Files:**

1. **[README.md](README.md)** - Full project documentation
2. **[QUICKSTART.md](QUICKSTART.md)** - 3-step getting started
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy online guide
4. **[GPT5_UPGRADE.md](GPT5_UPGRADE.md)** - GPT-5 migration details
5. **[MODEL_SELECTION.md](MODEL_SELECTION.md)** ⭐ NEW! - Model comparison
6. **[CHANGELOG.md](CHANGELOG.md)** - Version history

**All docs include:**
- Step-by-step instructions
- Code examples
- Troubleshooting tips
- Cost breakdowns

---

## 💰 Cost Breakdown

### Total Monthly Cost (Family Use):

| Component | Cost |
|-----------|------|
| **Streamlit Cloud** (hosting) | $0 (free tier) |
| **GPT-5-mini** (100 analyses) | ~$0.15 |
| **Total** | **~$0.15/month** 🎉 |

### With Premium GPT-5:

| Usage | GPT-5-mini | GPT-5 | Mixed (80/20) |
|-------|------------|-------|---------------|
| 50/month | $0.075 | $0.375 | $0.135 |
| 100/month | $0.15 | $0.75 | $0.27 |
| 500/month | $0.75 | $3.75 | $1.35 |

**Incredibly affordable for cutting-edge AI!**

---

## 🎛️ Model Selection Feature (NEW!)

### Web Interface Toggle

**How it Works:**
1. Enable AI Analysis checkbox
2. Enter OpenAI API key
3. Select model: GPT-5-mini or GPT-5
4. See live cost per analysis
5. Analyze product with chosen model

**Benefits:**
- ✅ No code changes
- ✅ Switch anytime
- ✅ Compare results easily
- ✅ Cost transparency
- ✅ Flexibility for different needs

**Use Cases:**
- Use GPT-5-mini for routine analyses
- Switch to GPT-5 for expensive purchases
- Compare both on suspicious products
- Let family choose based on budget

---

## 🔧 Technical Stack

**Backend:**
- Python 3.8+
- Beautiful Soup 4 (scraping)
- spaCy + TextBlob + NLTK (NLP)
- NumPy (statistics)
- OpenAI API (GPT-5)

**Frontend:**
- Streamlit (web interface)
- Mobile-responsive design
- Real-time updates

**Deployment:**
- Streamlit Cloud (free)
- GitHub integration
- Environment secrets

---

## 🎯 Use Cases

### Personal Shopper
- Check reviews before buying
- Avoid fake-review traps
- Find genuinely good products
- Save money on bad purchases

### Gift Buyer
- Research products for family
- Ensure quality before gifting
- Avoid disappointments
- Compare products reliably

### Professional Reviewer
- Analyze products for clients
- Detect manipulation campaigns
- Provide data-driven insights
- Generate detailed reports

### Seller/Brand
- Monitor your own products
- Detect competitor manipulation
- Track review authenticity over time
- Protect brand reputation

---

## 🚦 Getting Started (3 Steps)

### 1. Install
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure
```bash
cp .env.example .env
# Add OPENAI_API_KEY=sk-your-key
```

### 3. Run
```bash
streamlit run app.py
```

**Opens at http://localhost:8501** 🎉

---

## 📈 Roadmap

### Coming Soon:
- [ ] GPT-5-nano option in web UI
- [ ] Batch analysis (multiple products)
- [ ] Historical tracking
- [ ] PDF/HTML export

### Future:
- [ ] Browser extension
- [ ] More platforms (Yelp, Google)
- [ ] Machine learning classifier
- [ ] Public API

---

## ⭐ Why Project Veritas?

**Most Advanced:**
- Uses GPT-5 (released Aug 2025)
- 45% fewer hallucinations than GPT-4o
- 8 statistical + AI detectors

**Most Affordable:**
- ~$0.15/month (GPT-5-mini)
- Free hosting (Streamlit Cloud)
- No hidden costs

**Most Accessible:**
- Beautiful web interface
- Zero learning curve
- Mobile-friendly
- Family-shareable

**Most Flexible:**
- Toggle between AI models
- Highly configurable
- CLI + Web interface
- Open-source

---

## 🏆 Summary

**You have a production-ready, family-accessible, AI-powered fake review detector using the world's most advanced AI (GPT-5) for less than 20 cents per month!**

**Key Features:**
- ✅ Dual scoring (Trust + Quality)
- ✅ GPT-5 AI analysis with model toggle ⭐
- ✅ 8 red flag detectors
- ✅ Beautiful web interface
- ✅ Easy deployment
- ✅ Comprehensive docs
- ✅ Ultra-low cost

**Everything you need to fight fake reviews!** 🚀

---

**Ready to use?** See [QUICKSTART.md](QUICKSTART.md)

**Want to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)

**Questions about models?** See [MODEL_SELECTION.md](MODEL_SELECTION.md)
