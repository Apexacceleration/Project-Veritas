"""
Project Veritas - Analysis Engine
Implements 8 red flag detection algorithms for identifying fake/suspicious reviews
"""

import sys
import os
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src import utils


def check_review_velocity(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #1: Review Velocity Spike
    Detects suspicious bursts of reviews posted in short timeframes.

    Args:
        reviews (List[Dict]): List of review dictionaries with 'date' field

    Returns:
        Dict: {
            "triggered": bool,
            "score_impact": float,
            "details": str,
            "suspicious_reviews": List[Dict]
        }
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    # Filter reviews with valid dates
    dated_reviews = [r for r in reviews if r.get("date")]
    if len(dated_reviews) < 10:  # Need enough data
        result["details"] = "Insufficient data for velocity analysis"
        return result

    # Sort by date
    dated_reviews.sort(key=lambda x: x["date"])

    # Check for reviews within threshold window
    window_hours = config.VELOCITY_THRESHOLD_HOURS
    threshold_percentage = config.VELOCITY_THRESHOLD_PERCENTAGE

    # Sliding window analysis
    max_reviews_in_window = 0
    suspicious_window_reviews = []

    for i, review in enumerate(dated_reviews):
        window_start = review["date"]
        window_end = window_start + timedelta(hours=window_hours)

        # Count reviews in this window
        reviews_in_window = [
            r for r in dated_reviews
            if window_start <= r["date"] <= window_end
        ]

        if len(reviews_in_window) > max_reviews_in_window:
            max_reviews_in_window = len(reviews_in_window)
            suspicious_window_reviews = reviews_in_window

    # Calculate percentage
    percentage_in_window = max_reviews_in_window / len(dated_reviews)

    if percentage_in_window >= threshold_percentage:
        result["triggered"] = True
        result["score_impact"] = config.VELOCITY_PENALTY
        result["details"] = f"{max_reviews_in_window} reviews ({utils.format_percentage(percentage_in_window)}) posted within {window_hours} hours"
        result["suspicious_reviews"] = suspicious_window_reviews

    return result


def check_generic_praise(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #2: Generic Praise Pattern
    Detects vague, non-specific positive language without details.

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    generic_reviews = []

    for review in reviews:
        text = review.get("review_text", "").lower()
        title = review.get("title", "").lower()
        full_text = (title + " " + text).lower()

        # Check if review is too short
        if len(full_text.strip()) < config.GENERIC_MIN_LENGTH:
            generic_reviews.append(review)
            continue

        # Check for generic phrases
        for phrase in config.GENERIC_PHRASES:
            if phrase.lower() in full_text:
                # If it ONLY contains generic phrase and nothing else meaningful
                if len(full_text.split()) <= 10:  # Very short reviews with generic phrases
                    generic_reviews.append(review)
                    break

    if generic_reviews:
        result["triggered"] = True
        count = len(generic_reviews)
        result["score_impact"] = config.GENERIC_PENALTY_PER_REVIEW * count
        result["details"] = f"{count} reviews ({utils.format_percentage(count/len(reviews))}) are generic or too short"
        result["suspicious_reviews"] = generic_reviews

    return result


def check_suspicious_reviewers(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #3: Suspicious Reviewer Profile
    Detects reviewers with unusual patterns (many reviews in short time, only extreme ratings).

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    # Group reviews by author
    reviews_by_author = defaultdict(list)
    for review in reviews:
        author = review.get("author", "Anonymous")
        reviews_by_author[author].append(review)

    suspicious_authors = []
    suspicious_reviews = []

    for author, author_reviews in reviews_by_author.items():
        if len(author_reviews) < 2:  # Need multiple reviews to detect pattern
            continue

        # Check for suspicious patterns:

        # Pattern 1: Check if all ratings are the same (e.g., all 5-star)
        ratings = [r.get("rating") for r in author_reviews if r.get("rating")]
        if ratings:
            rating_counts = Counter(ratings)
            most_common_rating_count = rating_counts.most_common(1)[0][1]
            same_rating_percentage = most_common_rating_count / len(ratings)

            if same_rating_percentage >= config.REVIEWER_RED_FLAGS["same_rating_percentage"]:
                suspicious_authors.append(author)
                suspicious_reviews.extend(author_reviews)

    # Calculate percentage
    if suspicious_authors:
        suspicious_percentage = len(suspicious_authors) / len(reviews_by_author)

        if suspicious_percentage >= config.SUSPICIOUS_REVIEWER_THRESHOLD:
            result["triggered"] = True
            result["score_impact"] = config.SUSPICIOUS_REVIEWER_PENALTY
            result["details"] = f"{len(suspicious_authors)} reviewers ({utils.format_percentage(suspicious_percentage)}) show suspicious patterns"
            result["suspicious_reviews"] = suspicious_reviews

    return result


def check_linguistic_anomalies(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #4: Linguistic Anomalies
    Detects unnatural language patterns, keyword stuffing, poor grammar.

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    anomalous_reviews = []

    for review in reviews:
        text = review.get("review_text", "")
        if not text or len(text.split()) < 10:
            continue

        is_anomalous = False

        # Check for keyword stuffing (same word repeated many times)
        words = text.lower().split()
        word_counts = Counter(words)

        # Ignore common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "was", "are", "this", "that", "it"}

        for word, count in word_counts.items():
            if word not in common_words and len(word) > 3:
                if count >= config.KEYWORD_STUFFING_THRESHOLD:
                    is_anomalous = True
                    break

        # Check for excessive punctuation (!!!!, ????)
        if re.search(r'[!?]{4,}', text):
            is_anomalous = True

        # Check for ALL CAPS (more than 30% of text)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3 and len(text) > 20:
            is_anomalous = True

        if is_anomalous:
            anomalous_reviews.append(review)

    if anomalous_reviews:
        result["triggered"] = True
        count = len(anomalous_reviews)
        result["score_impact"] = config.LINGUISTIC_PENALTY_PER_REVIEW * count
        result["details"] = f"{count} reviews ({utils.format_percentage(count/len(reviews))}) show linguistic anomalies"
        result["suspicious_reviews"] = anomalous_reviews

    return result


def check_sentiment_imbalance(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #5: Extreme Sentiment Imbalance
    Detects disproportionate ratios of 5-star vs other ratings (bimodal distribution).

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    # Count ratings
    ratings = [r.get("rating") for r in reviews if r.get("rating")]
    if not ratings:
        return result

    rating_counts = Counter(ratings)
    total = len(ratings)

    # Calculate percentages
    five_star_pct = rating_counts.get(5.0, 0) / total
    one_star_pct = rating_counts.get(1.0, 0) / total

    # Check for extreme 5-star dominance
    if five_star_pct >= config.FIVE_STAR_THRESHOLD:
        result["triggered"] = True
        result["score_impact"] = config.SENTIMENT_IMBALANCE_PENALTY
        result["details"] = f"Extreme 5-star dominance: {utils.format_percentage(five_star_pct)} of reviews are 5-star"

    # Check for bimodal distribution (lots of 5-star AND lots of 1-star, few middle)
    elif (five_star_pct >= config.BIMODAL_THRESHOLD and
          one_star_pct >= config.BIMODAL_THRESHOLD and
          (five_star_pct + one_star_pct) > 0.80):
        result["triggered"] = True
        result["score_impact"] = config.SENTIMENT_IMBALANCE_PENALTY
        result["details"] = f"Bimodal distribution detected: {utils.format_percentage(five_star_pct)} 5-star, {utils.format_percentage(one_star_pct)} 1-star"

    # Mark 5-star reviews as suspicious if triggered
    if result["triggered"]:
        result["suspicious_reviews"] = [r for r in reviews if r.get("rating") == 5.0]

    return result


def check_review_length_extremes(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #6: Review Length Extremes
    Detects unusually short or suspiciously long reviews.

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    extreme_reviews = []

    for review in reviews:
        length = review.get("review_length", 0)

        if length < config.REVIEW_LENGTH_MIN or length > config.REVIEW_LENGTH_MAX:
            extreme_reviews.append(review)

    if extreme_reviews:
        result["triggered"] = True
        count = len(extreme_reviews)
        result["score_impact"] = config.LENGTH_EXTREME_PENALTY_PER_REVIEW * count
        result["details"] = f"{count} reviews ({utils.format_percentage(count/len(reviews))}) are extremely short or long"
        result["suspicious_reviews"] = extreme_reviews

    return result


def check_verified_ratio(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #7: Verified Purchase Ratio
    Checks the percentage of reviews with "Verified Purchase" badge.

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary (can also trigger BONUS)
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    verified_count = sum(1 for r in reviews if r.get("verified_purchase", False))
    total = len(reviews)

    verified_ratio = utils.safe_divide(verified_count, total)

    # Low verified ratio is suspicious
    if verified_ratio < config.VERIFIED_LOW_THRESHOLD:
        result["triggered"] = True
        result["score_impact"] = config.VERIFIED_LOW_PENALTY
        result["details"] = f"Low verified purchase rate: only {utils.format_percentage(verified_ratio)} are verified"
        # Mark non-verified reviews as suspicious
        result["suspicious_reviews"] = [r for r in reviews if not r.get("verified_purchase", False)]

    # High verified ratio is a GOOD sign (bonus)
    elif verified_ratio >= config.VERIFIED_HIGH_THRESHOLD:
        result["triggered"] = True  # "Triggered" but in a good way
        result["score_impact"] = config.VERIFIED_HIGH_BONUS
        result["details"] = f"High verified purchase rate: {utils.format_percentage(verified_ratio)} are verified (BONUS)"

    return result


def check_repetitive_phrases(reviews: List[Dict]) -> Dict:
    """
    RED FLAG #8: Repetitive Phrasing
    Detects identical or near-identical phrases across multiple reviews.

    Args:
        reviews (List[Dict]): List of review dictionaries

    Returns:
        Dict: Red flag result dictionary
    """
    result = {
        "triggered": False,
        "score_impact": 0,
        "details": "",
        "suspicious_reviews": []
    }

    # Extract n-grams from all reviews
    ngram_to_reviews = defaultdict(list)

    for review in reviews:
        text = review.get("review_text", "") + " " + review.get("title", "")
        ngrams = utils.get_ngrams(text, n=config.REPETITIVE_PHRASE_MIN_LENGTH)

        for ngram in ngrams:
            ngram_to_reviews[ngram].append(review)

    # Find phrases that appear in multiple reviews
    repeated_phrases = []
    suspicious_reviews = []

    for ngram, ngram_reviews in ngram_to_reviews.items():
        if len(ngram_reviews) >= config.REPETITIVE_PHRASE_COUNT:
            repeated_phrases.append((ngram, len(ngram_reviews)))
            suspicious_reviews.extend(ngram_reviews)

    # Remove duplicates
    suspicious_reviews = list({r["review_text"]: r for r in suspicious_reviews}.values())

    if repeated_phrases:
        result["triggered"] = True
        result["score_impact"] = config.REPETITIVE_PHRASE_PENALTY
        # Show top repeated phrase
        top_phrase = sorted(repeated_phrases, key=lambda x: x[1], reverse=True)[0]
        result["details"] = f"Repetitive phrases detected: '{top_phrase[0]}' appears in {top_phrase[1]} reviews"
        result["suspicious_reviews"] = suspicious_reviews

    return result


def analyze_data(reviews: List[Dict]) -> Dict:
    """
    Main analysis function. Runs all 8 red flag checks.

    Args:
        reviews (List[Dict]): List of review dictionaries from scraper

    Returns:
        Dict: Complete analysis report with all red flags
        {
            "total_reviews": int,
            "red_flags": {
                "review_velocity": {...},
                "generic_praise": {...},
                "suspicious_reviewers": {...},
                "linguistic_anomalies": {...},
                "sentiment_imbalance": {...},
                "review_length_extremes": {...},
                "verified_ratio": {...},
                "repetitive_phrases": {...}
            },
            "total_score_impact": float,
            "triggered_flags": List[str]
        }
    """
    print(f"\n🔍 Running analysis on {len(reviews)} reviews...")

    analysis_report = {
        "total_reviews": len(reviews),
        "red_flags": {},
        "total_score_impact": 0,
        "triggered_flags": []
    }

    # Run all 8 checks
    checks = {
        "review_velocity": check_review_velocity,
        "generic_praise": check_generic_praise,
        "suspicious_reviewers": check_suspicious_reviewers,
        "linguistic_anomalies": check_linguistic_anomalies,
        "sentiment_imbalance": check_sentiment_imbalance,
        "review_length_extremes": check_review_length_extremes,
        "verified_ratio": check_verified_ratio,
        "repetitive_phrases": check_repetitive_phrases
    }

    for flag_name, check_function in checks.items():
        print(f"  ⚡ Checking: {flag_name.replace('_', ' ').title()}")
        result = check_function(reviews)
        analysis_report["red_flags"][flag_name] = result

        # Track impact and triggered flags
        if result["triggered"]:
            analysis_report["total_score_impact"] += result["score_impact"]
            if result["score_impact"] < 0:  # Penalty
                analysis_report["triggered_flags"].append(flag_name)
            print(f"     ⚠️  {result['details']} (Impact: {result['score_impact']:+.1f})")
        else:
            print(f"     ✓ No issues detected")

    print(f"\n📊 Analysis complete. Total score impact: {analysis_report['total_score_impact']:+.1f}")
    print(f"🚩 Flags triggered: {len(analysis_report['triggered_flags'])}")

    return analysis_report


# Example usage
if __name__ == "__main__":
    # Test with dummy data
    test_reviews = [
        {
            "rating": 5.0,
            "title": "Great!",
            "review_text": "Great product!",
            "date": datetime.now(),
            "author": "TestUser1",
            "verified_purchase": False,
            "has_images": False,
            "review_length": 20
        }
    ] * 100  # Simulate 100 identical reviews

    report = analyze_data(test_reviews)
    print(f"\nTriggered flags: {report['triggered_flags']}")
