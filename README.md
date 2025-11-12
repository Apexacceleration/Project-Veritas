# 🔍 Project Veritas

> **Finding truth in a world that wants to hide it—at least in online reviews.**

Project Veritas is a powerful review analysis tool that detects fake, incentivized, and manipulated reviews on Amazon products. Using advanced statistical analysis, AI-powered linguistic detection, and a beautiful web interface, it provides two key scores:

- **🔒 Trust Score**: Measures the reliability of the review dataset
- **⭐ Quality Score**: Measures actual product quality based on trusted reviews only

## ✨ Features

- 🌐 **Beautiful Web Interface** - Easy for anyone to use (Streamlit)
- 🤖 **AI-Powered Analysis** - Optional OpenAI integration for enhanced detection
- 📊 **Dual Scoring System** - Trust + Quality scores with letter grades
- 🔍 **8 Red Flag Detectors** - Statistical and linguistic analysis
- 📱 **Mobile-Friendly** - Works on any device
- 💰 **Low Cost** - ~$0.50/month for typical family use
- 🚀 **Easy Deployment** - Free hosting on Streamlit Cloud

---

## 🚀 Quick Start

### Web Interface (Recommended)

1. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Set up OpenAI API** (optional but recommended)
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Run the web app**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501` 🎉

### Command Line (Power Users)

```bash
python src/main.py https://amazon.com/dp/B08N5WRWNW
```

Save report to file:
```bash
python src/main.py https://amazon.com/dp/B08N5WRWNW --output report.json
```

### Python Script

```python
from src.main import run_veritas

# Analyze a product
report = run_veritas("https://amazon.com/dp/B08N5WRWNW")

print(f"Trust Score: {report['trust_score']} ({report['trust_grade']})")
print(f"Quality Score: {report['quality_score']} ({report['quality_grade']})")
```

**📖 See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions**
**🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for online deployment guide**

---

## 📊 How It Works

### Phase 1: Scraping
- Scrapes Amazon product reviews with anti-bot measures
- Extracts: rating, text, date, author, verified purchase status, images
- Implements random delays and user-agent rotation to avoid detection

### Phase 2: Analysis (8 Red Flag Checks)

1. **Review Velocity Spike** - Detects unnatural bursts of reviews in short timeframes
2. **Generic Praise Pattern** - Identifies vague, non-specific positive language
3. **Suspicious Reviewer Profile** - Flags reviewers with unusual patterns
4. **Linguistic Anomalies** - Detects keyword stuffing, poor grammar, unnatural language
5. **Extreme Sentiment Imbalance** - Identifies disproportionate 5-star ratios
6. **Review Length Extremes** - Flags suspiciously short or long reviews
7. **Verified Purchase Ratio** - Analyzes percentage of verified purchases
8. **Repetitive Phrasing** - Detects identical phrases across multiple reviews

### Phase 3: Scoring

#### Trust Score (0-100)
- Starts at 100 (perfect trust)
- Applies penalties for each red flag detected
- Adds bonuses for positive signals (verified purchases, user images, detailed reviews)
- Converted to letter grade (A-F)

#### Quality Score (0-100)
- Filters out suspicious reviews
- Analyzes only trusted reviews for product quality
- Based on average star rating + sentiment analysis
- Adjusts for consistency, detail level, and negative keywords

---

## 📋 Output Format

```json
{
  "project": "Project Veritas",
  "url": "https://amazon.com/dp/B08N5WRWNW",
  "trust_score": 68.5,
  "trust_grade": "C",
  "trust_summary": "Mixed signals detected. 3 red flag(s) present. Proceed with caution. Issues include: Review Velocity, Generic Praise, Low Verified Ratio",
  "quality_score": 82.0,
  "quality_grade": "B",
  "quality_summary": "Good product quality. Based on 127 trusted reviews, average 4.2-star rating with generally positive feedback.",
  "total_reviews_analyzed": 250,
  "trusted_reviews_count": 127,
  "suspicious_reviews_count": 123,
  "red_flags_triggered": [
    "Review Velocity",
    "Generic Praise",
    "Verified Ratio"
  ]
}
```

---

## ⚙️ Configuration

All thresholds and weights can be customized in [`config.py`](config.py):

```python
# Example: Adjust penalty for review velocity spike
VELOCITY_PENALTY = -15  # Change to -20 for stricter penalty

# Example: Change verified purchase threshold
VERIFIED_LOW_THRESHOLD = 0.50  # 50% minimum
```

---

## 🛡️ Anti-Scraping Resilience

Project Veritas implements several measures to avoid detection:

- **Rotating User Agents** - Simulates different browsers
- **Random Delays** - 2-5 second delays between requests
- **Request Headers** - Mimics legitimate browser requests
- **Error Handling** - Gracefully handles timeouts and blocks

### Using Proxies (Optional)

For heavy usage, configure proxies in `.env`:

```bash
cp .env.example .env
# Edit .env and add your proxy settings
PROXY_HTTP=http://username:password@proxy-server:port
PROXY_HTTPS=https://username:password@proxy-server:port
```

---

## 📁 Project Structure

```
project-veritas/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Master orchestrator (run_veritas)
│   ├── scraper.py           # Amazon review scraper
│   ├── analyzer.py          # 8 red flag detection functions
│   ├── scorer.py            # Trust & Quality scoring system
│   └── utils.py             # Helper functions
├── config.py                # Configuration (thresholds, weights)
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment config
└── README.md                # This file
```

---

## 🔧 Development

### Running Tests

```bash
# Test scraper
python src/scraper.py

# Test analyzer
python src/analyzer.py

# Test scorer
python src/scorer.py
```

### Adding New Red Flags

1. Create detection function in [`src/analyzer.py`](src/analyzer.py)
2. Add configuration values to [`config.py`](config.py)
3. Register function in `analyze_data()` checks dictionary

---

## ⚠️ Limitations & Disclaimer

- **Amazon Terms of Service**: Web scraping may violate Amazon's ToS. Use responsibly and at your own risk.
- **Detection Accuracy**: No system is 100% accurate. False positives/negatives may occur.
- **Anti-Scraping**: Amazon actively blocks scrapers. Consider using commercial APIs for production.
- **Legal**: This tool is for educational/research purposes. Not intended for commercial use without proper authorization.

---

## 🎯 Roadmap

### Future Enhancements
- [ ] Support for other platforms (Yelp, Google Reviews, Best Buy)
- [ ] Machine learning model for more sophisticated fake review detection
- [ ] Web interface / dashboard
- [ ] Browser extension
- [ ] API service
- [ ] Historical tracking (monitor reviews over time)

---

## 📚 Research & Methodology

Project Veritas is based on research from:

- **Fakespot** methodology (before its 2025 shutdown)
- Academic papers on fake review detection using linguistic analysis
- Amazon's own AI-based fake review detection patterns
- Industry best practices for review authenticity analysis

Key research areas:
- Psycholinguistic markers in deceptive text
- Statistical anomaly detection in review patterns
- Sentiment analysis and emotional exaggeration
- Behavioral patterns of fake reviewers

---

## 🤝 Contributing

Contributions welcome! Areas to improve:

1. **Better scraping resilience** - Handle CAPTCHA, improve anti-bot evasion
2. **More red flags** - Add additional detection algorithms
3. **ML models** - Train classifiers on labeled fake review datasets
4. **Platform support** - Extend to other review platforms
5. **Documentation** - Improve docs and add examples

---

## 📄 License

This project is released under the MIT License. See LICENSE file for details.

---

## 👨‍💻 Author

Built with 🧠 and ☕ for the mission of finding truth in online reviews.

**Project Veritas** - *"In vino veritas, in reviews... well, that's what we're here to find out."*

---

## 🆘 Support

Having issues?

1. Check the [Troubleshooting](#troubleshooting) section below
2. Review the [Configuration](#configuration) options
3. Open an issue on GitHub with details about your error

### Troubleshooting

**"Amazon blocked my requests"**
- Reduce scraping frequency in `config.py` (increase delays)
- Use proxies (see [Anti-Scraping](#anti-scraping-resilience))
- Consider commercial scraping APIs

**"No reviews found"**
- Verify the product URL is correct
- Check if product has reviews on Amazon
- Product might be region-locked

**"Import errors"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Download spaCy model: `python -m spacy download en_core_web_sm`

**"Scores seem off"**
- Adjust thresholds in `config.py` based on your needs
- Some products naturally have skewed distributions
- Check the red flags triggered for details

---

**Made with ❤️ for truth-seekers everywhere**
