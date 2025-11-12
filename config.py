"""
Project Veritas - Configuration File
Contains all thresholds, weights, and scoring parameters from Phase 1 Logic
"""

# ============================================================================
# AI CONFIGURATION
# ============================================================================
# GPT-5 Models (Released August 2025):
# - "gpt-5": Best reasoning (74.9% SWE-bench, 45% fewer hallucinations)
# - "gpt-5-mini": Balanced cost/performance (RECOMMENDED for most use)
# - "gpt-5-nano": Ultra-low cost option
#
# Pricing (as of Aug 2025):
# - GPT-5: $1.25/1M input tokens, $10/1M output tokens
# - GPT-5-mini: Lower cost (specific pricing TBD)
#
# Why GPT-5-mini for reviews:
# - Superior reasoning vs GPT-4o-mini
# - 45% fewer hallucinations = more reliable fake review detection
# - Excellent cost/performance ratio
# - Adaptive reasoning levels (minimal/low/medium/high)

OPENAI_MODEL = "gpt-5-mini"  # Recommended: Best balance of accuracy and cost
# Alternative options:
# OPENAI_MODEL = "gpt-5"      # Premium: Best accuracy, higher cost
# OPENAI_MODEL = "gpt-5-nano" # Budget: Lowest cost

# Note: Set OPENAI_API_KEY in .env file or environment variable

# ============================================================================
# SCORING SYSTEM - Starting Score
# ============================================================================
STARTING_TRUST_SCORE = 100

# ============================================================================
# RED FLAG THRESHOLDS & PENALTIES
# ============================================================================

# 1. Review Velocity Spike
VELOCITY_THRESHOLD_HOURS = 72  # Suspicious if >30% reviews within this window
VELOCITY_THRESHOLD_PERCENTAGE = 0.30  # 30% of reviews
VELOCITY_PENALTY = -15

# 2. Generic Praise Pattern
GENERIC_PHRASES = [
    "great product", "amazing", "best purchase", "highly recommend",
    "love it", "perfect", "excellent", "awesome", "fantastic",
    "incredible", "superb", "wonderful", "exceeded expectations"
]
GENERIC_MIN_LENGTH = 30  # Characters - reviews shorter than this are suspicious
GENERIC_PENALTY_PER_REVIEW = -1

# 3. Suspicious Reviewer Profile
SUSPICIOUS_REVIEWER_THRESHOLD = 0.20  # 20% of reviewers show red flags
SUSPICIOUS_REVIEWER_PENALTY = -10
REVIEWER_RED_FLAGS = {
    "reviews_in_short_time": 10,  # >10 reviews in 7 days
    "days_window": 7,
    "same_rating_percentage": 0.90  # >90% of reviews are same rating (e.g., all 5-star)
}

# 4. Linguistic Anomalies
KEYWORD_STUFFING_THRESHOLD = 5  # Same keyword repeated >5 times
LINGUISTIC_PENALTY_PER_REVIEW = -0.5

# 5. Extreme Sentiment Imbalance
FIVE_STAR_THRESHOLD = 0.75  # >75% five-star reviews is suspicious
BIMODAL_THRESHOLD = 0.30  # If 5-star + 1-star make up >80% and each >30%
SENTIMENT_IMBALANCE_PENALTY = -20

# 6. Review Length Extremes
REVIEW_LENGTH_MIN = 20  # Characters
REVIEW_LENGTH_MAX = 400  # Characters
LENGTH_EXTREME_PENALTY_PER_REVIEW = -0.5

# 7. Verified Purchase Ratio
VERIFIED_LOW_THRESHOLD = 0.50  # <50% verified is suspicious
VERIFIED_HIGH_THRESHOLD = 0.80  # >80% verified is good
VERIFIED_LOW_PENALTY = -15
VERIFIED_HIGH_BONUS = +5

# 8. Repetitive Phrasing
REPETITIVE_PHRASE_MIN_LENGTH = 4  # Words in phrase
REPETITIVE_PHRASE_COUNT = 5  # If same phrase appears in >5 reviews
REPETITIVE_PHRASE_PENALTY = -10

# ============================================================================
# BONUS POINTS (Trust Score)
# ============================================================================

# User-uploaded images
IMAGE_BONUS_PER_REVIEW = +0.5

# Detailed reviews (specific length range)
DETAILED_REVIEW_MIN_LENGTH = 75
DETAILED_REVIEW_MAX_LENGTH = 250
DETAILED_REVIEW_BONUS = +0.3

# Balanced distribution (normal bell curve)
BALANCED_DISTRIBUTION_BONUS = +10
BALANCED_DISTRIBUTION_CRITERIA = {
    "three_star_min": 0.15,  # At least 15% 3-star
    "four_star_min": 0.20,   # At least 20% 4-star
    "five_star_max": 0.50    # No more than 50% 5-star
}

# ============================================================================
# QUALITY SCORE CALCULATION (Based on Trusted Reviews Only)
# ============================================================================

# Star rating conversion to 0-100 scale
STAR_TO_SCORE_MULTIPLIER = 20  # 5 stars = 100, 4 stars = 80, etc.

# Quality bonuses
QUALITY_CONSISTENT_BONUS = +5  # Low variance in ratings
QUALITY_DETAILED_BONUS = +3    # Specific, detailed feedback
QUALITY_VARIANCE_THRESHOLD = 0.5  # Standard deviation threshold for consistency

# Quality penalties
QUALITY_NEGATIVE_KEYWORDS = [
    "defective", "broke", "broken", "returned", "refund", "disappointed",
    "waste", "terrible", "awful", "poor quality", "cheap", "scam"
]
QUALITY_NEGATIVE_PENALTY = -5
QUALITY_HIGH_VARIANCE_PENALTY = -3

# ============================================================================
# GRADE SCALE (Applies to both Trust and Quality Scores)
# ============================================================================

GRADE_SCALE = {
    90: "A",  # 90-100
    75: "B",  # 75-89
    60: "C",  # 60-74
    45: "D",  # 45-59
    0:  "F"   # 0-44
}

# ============================================================================
# SCRAPER SETTINGS
# ============================================================================

# Anti-scraping measures
REQUEST_MIN_DELAY = 2.0  # Seconds
REQUEST_MAX_DELAY = 5.0  # Seconds
REQUEST_TIMEOUT = 10     # Seconds

# Maximum reviews to scrape (for MVP)
MAX_REVIEWS_TO_SCRAPE = 500

# User agents for rotation (simulate real browsers)
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]
