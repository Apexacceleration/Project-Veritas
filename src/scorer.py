"""
Project Veritas - Scoring Module
Calculates Trust Score (review reliability) and Quality Score (product quality from trusted reviews)
"""

import sys
import os
from typing import List, Dict, Tuple
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src import utils


def calculate_trust_score(analysis_report: Dict) -> Tuple[float, str, str]:
    """
    Calculates Trust Score based on red flag analysis.
    Measures the reliability of the review dataset.

    Args:
        analysis_report (Dict): Analysis report from analyzer.py

    Returns:
        Tuple[float, str, str]: (score, grade, summary)
    """
    print("\n🎯 Calculating Trust Score...")

    # Start with perfect score
    score = config.STARTING_TRUST_SCORE

    # Apply all score impacts from red flags
    score += analysis_report["total_score_impact"]

    # Calculate bonuses that aren't handled by red flags

    reviews = []  # We'll need to pass reviews for bonus calculations
    red_flags = analysis_report["red_flags"]

    # Bonus for user-uploaded images (if we have access to review data)
    # This is calculated in the main function where we have access to reviews

    # Ensure score stays within bounds
    score = max(0, min(100, score))

    # Calculate grade
    grade = utils.calculate_grade(score)

    # Generate summary
    triggered_count = len(analysis_report["triggered_flags"])

    if score >= 90:
        summary = "Highly trustworthy reviews. No significant red flags detected."
    elif score >= 75:
        summary = f"Generally reliable reviews with {triggered_count} minor red flag(s) detected."
    elif score >= 60:
        summary = f"Mixed signals detected. {triggered_count} red flag(s) present. Proceed with caution."
    elif score >= 45:
        summary = f"Significant red flags detected. {triggered_count} suspicious pattern(s) found."
    else:
        summary = f"High likelihood of manipulation. {triggered_count} major red flag(s) triggered."

    # Add specific red flag details to summary
    if analysis_report["triggered_flags"]:
        flag_names = [flag.replace("_", " ").title() for flag in analysis_report["triggered_flags"]]
        summary += f" Issues include: {', '.join(flag_names[:3])}"  # Show top 3
        if len(flag_names) > 3:
            summary += f", and {len(flag_names) - 3} more"

    print(f"   Trust Score: {score:.1f} ({grade})")
    print(f"   Summary: {summary}")

    return score, grade, summary


def filter_trusted_reviews(reviews: List[Dict], analysis_report: Dict) -> List[Dict]:
    """
    Filters out suspicious reviews to create a 'trusted subset'.
    Used for calculating Quality Score.

    Args:
        reviews (List[Dict]): All reviews
        analysis_report (Dict): Analysis report with red flags

    Returns:
        List[Dict]: List of trusted reviews only
    """
    print("\n🔍 Filtering trusted reviews...")

    # Collect all suspicious review IDs
    suspicious_reviews_set = set()

    for flag_name, flag_result in analysis_report["red_flags"].items():
        if flag_result["triggered"] and flag_result.get("suspicious_reviews"):
            # Use review_text as unique identifier (not perfect but works for MVP)
            for review in flag_result["suspicious_reviews"]:
                suspicious_reviews_set.add(review.get("review_text", ""))

    # Filter out suspicious reviews
    trusted_reviews = []
    for review in reviews:
        review_text = review.get("review_text", "")
        if review_text not in suspicious_reviews_set:
            trusted_reviews.append(review)

    print(f"   Total reviews: {len(reviews)}")
    print(f"   Suspicious reviews: {len(suspicious_reviews_set)}")
    print(f"   Trusted reviews: {len(trusted_reviews)}")

    return trusted_reviews


def calculate_quality_score(trusted_reviews: List[Dict]) -> Tuple[float, str, str]:
    """
    Calculates Quality Score based on trusted reviews only.
    Measures actual product quality after filtering out fake reviews.

    Args:
        trusted_reviews (List[Dict]): List of trusted reviews (after filtering)

    Returns:
        Tuple[float, str, str]: (score, grade, summary)
    """
    print("\n⭐ Calculating Quality Score...")

    if not trusted_reviews:
        print("   ⚠️  No trusted reviews available for quality analysis")
        return 0, "F", "Insufficient trusted reviews to assess product quality"

    # Start with average star rating converted to 0-100 scale
    ratings = [r.get("rating", 0) for r in trusted_reviews if r.get("rating")]

    if not ratings:
        return 0, "F", "No valid ratings in trusted reviews"

    avg_rating = np.mean(ratings)
    score = avg_rating * config.STAR_TO_SCORE_MULTIPLIER

    print(f"   Average rating: {avg_rating:.2f} stars -> Base score: {score:.1f}")

    # Calculate variance (consistency)
    rating_variance = np.var(ratings)
    rating_std = np.std(ratings)

    # BONUS: Consistent ratings (low variance)
    if rating_std < config.QUALITY_VARIANCE_THRESHOLD:
        score += config.QUALITY_CONSISTENT_BONUS
        print(f"   ✓ Consistent ratings bonus: +{config.QUALITY_CONSISTENT_BONUS}")

    # PENALTY: High variance (inconsistent quality)
    elif rating_std > 1.0:
        score += config.QUALITY_HIGH_VARIANCE_PENALTY
        print(f"   ⚠️  High variance penalty: {config.QUALITY_HIGH_VARIANCE_PENALTY}")

    # BONUS: Detailed reviews
    detailed_count = sum(
        1 for r in trusted_reviews
        if config.DETAILED_REVIEW_MIN_LENGTH <= r.get("review_length", 0) <= config.DETAILED_REVIEW_MAX_LENGTH
    )
    detailed_percentage = detailed_count / len(trusted_reviews)

    if detailed_percentage > 0.5:  # More than 50% are detailed
        score += config.QUALITY_DETAILED_BONUS
        print(f"   ✓ Detailed reviews bonus: +{config.QUALITY_DETAILED_BONUS}")

    # PENALTY: Negative keywords in trusted reviews
    negative_keyword_count = 0
    for review in trusted_reviews:
        text = (review.get("review_text", "") + " " + review.get("title", "")).lower()
        for keyword in config.QUALITY_NEGATIVE_KEYWORDS:
            if keyword in text:
                negative_keyword_count += 1
                break  # Count each review only once

    negative_percentage = negative_keyword_count / len(trusted_reviews)

    if negative_percentage > 0.3:  # More than 30% mention negative keywords
        score += config.QUALITY_NEGATIVE_PENALTY
        print(f"   ⚠️  Negative feedback penalty: {config.QUALITY_NEGATIVE_PENALTY}")

    # Ensure score stays within bounds
    score = max(0, min(100, score))

    # Calculate grade
    grade = utils.calculate_grade(score)

    # Generate summary
    if score >= 90:
        summary = f"Excellent product quality. Trusted reviews show consistent {avg_rating:.1f}-star ratings with detailed positive feedback."
    elif score >= 75:
        summary = f"Good product quality. Based on {len(trusted_reviews)} trusted reviews, average {avg_rating:.1f}-star rating with generally positive feedback."
    elif score >= 60:
        summary = f"Decent product quality with some concerns. {len(trusted_reviews)} trusted reviews average {avg_rating:.1f} stars, with mixed feedback."
    elif score >= 45:
        summary = f"Below average quality. Trusted reviews show {avg_rating:.1f}-star rating with notable complaints."
    else:
        summary = f"Poor product quality. Based on {len(trusted_reviews)} trusted reviews averaging {avg_rating:.1f} stars, with significant negative feedback."

    print(f"   Quality Score: {score:.1f} ({grade})")
    print(f"   Summary: {summary}")

    return score, grade, summary


def calculate_additional_bonuses(reviews: List[Dict]) -> float:
    """
    Calculates additional bonus points for Trust Score.
    (Image uploads, detailed reviews, balanced distribution)

    Args:
        reviews (List[Dict]): All reviews

    Returns:
        float: Total bonus points to add to Trust Score
    """
    bonus = 0

    # Bonus for user-uploaded images
    image_count = sum(1 for r in reviews if r.get("has_images", False))
    if image_count > 0:
        image_bonus = image_count * config.IMAGE_BONUS_PER_REVIEW
        bonus += image_bonus
        print(f"   ✓ User images bonus: +{image_bonus:.1f} ({image_count} reviews with images)")

    # Bonus for detailed reviews
    detailed_count = sum(
        1 for r in reviews
        if config.DETAILED_REVIEW_MIN_LENGTH <= r.get("review_length", 0) <= config.DETAILED_REVIEW_MAX_LENGTH
    )
    if detailed_count > 0:
        detailed_bonus = detailed_count * config.DETAILED_REVIEW_BONUS
        bonus += detailed_bonus
        print(f"   ✓ Detailed reviews bonus: +{detailed_bonus:.1f} ({detailed_count} detailed reviews)")

    # Bonus for balanced distribution
    ratings = [r.get("rating", 0) for r in reviews if r.get("rating")]
    if ratings:
        from collections import Counter
        rating_counts = Counter(ratings)
        total = len(ratings)

        three_star_pct = rating_counts.get(3.0, 0) / total
        four_star_pct = rating_counts.get(4.0, 0) / total
        five_star_pct = rating_counts.get(5.0, 0) / total

        criteria = config.BALANCED_DISTRIBUTION_CRITERIA

        if (three_star_pct >= criteria["three_star_min"] and
            four_star_pct >= criteria["four_star_min"] and
            five_star_pct <= criteria["five_star_max"]):
            bonus += config.BALANCED_DISTRIBUTION_BONUS
            print(f"   ✓ Balanced distribution bonus: +{config.BALANCED_DISTRIBUTION_BONUS}")

    return bonus


def generate_full_report(reviews: List[Dict], analysis_report: Dict, url: str) -> Dict:
    """
    Generates the complete Project Veritas report with both Trust and Quality scores.

    Args:
        reviews (List[Dict]): All scraped reviews
        analysis_report (Dict): Red flag analysis report
        url (str): Product URL

    Returns:
        Dict: Complete JSON report in Project Veritas format
    """
    print("\n" + "="*60)
    print("📊 GENERATING FINAL REPORT")
    print("="*60)

    # Calculate Trust Score
    trust_score, trust_grade, trust_summary = calculate_trust_score(analysis_report)

    # Add bonuses to trust score
    bonus_points = calculate_additional_bonuses(reviews)
    trust_score = min(100, trust_score + bonus_points)
    trust_grade = utils.calculate_grade(trust_score)  # Recalculate grade after bonuses

    # Filter trusted reviews
    trusted_reviews = filter_trusted_reviews(reviews, analysis_report)

    # Calculate Quality Score
    quality_score, quality_grade, quality_summary = calculate_quality_score(trusted_reviews)

    # Build red flags list (human-readable names)
    red_flags_triggered = []
    for flag_name in analysis_report["triggered_flags"]:
        human_name = flag_name.replace("_", " ").title()
        red_flags_triggered.append(human_name)

    # Construct final report
    report = {
        "project": "Project Veritas",
        "url": url,
        "trust_score": round(trust_score, 1),
        "trust_grade": trust_grade,
        "trust_summary": trust_summary,
        "quality_score": round(quality_score, 1),
        "quality_grade": quality_grade,
        "quality_summary": quality_summary,
        "total_reviews_analyzed": len(reviews),
        "trusted_reviews_count": len(trusted_reviews),
        "suspicious_reviews_count": len(reviews) - len(trusted_reviews),
        "red_flags_triggered": red_flags_triggered
    }

    print("\n" + "="*60)
    print("✅ REPORT COMPLETE")
    print("="*60)
    print(f"🔒 Trust Score: {trust_score:.1f} ({trust_grade})")
    print(f"⭐ Quality Score: {quality_score:.1f} ({quality_grade})")
    print(f"📊 Reviews: {len(reviews)} total, {len(trusted_reviews)} trusted")
    print(f"🚩 Red Flags: {len(red_flags_triggered)}")
    print("="*60 + "\n")

    return report


# Example usage
if __name__ == "__main__":
    # Test with dummy data
    from datetime import datetime

    test_reviews = [
        {
            "rating": 5.0,
            "title": "Great product",
            "review_text": "This is an amazing product that works exactly as described. Highly recommend!",
            "date": datetime.now(),
            "author": "TestUser1",
            "verified_purchase": True,
            "has_images": True,
            "review_length": 85
        },
        {
            "rating": 4.0,
            "title": "Good",
            "review_text": "Pretty good overall, minor issues but nothing major.",
            "date": datetime.now(),
            "author": "TestUser2",
            "verified_purchase": True,
            "has_images": False,
            "review_length": 55
        }
    ] * 50

    # Simulate analysis report
    test_analysis = {
        "total_reviews": len(test_reviews),
        "red_flags": {},
        "total_score_impact": -5,
        "triggered_flags": ["generic_praise"]
    }

    report = generate_full_report(test_reviews, test_analysis, "https://amazon.com/test")
    print("\nFinal Report:")
    import json
    print(json.dumps(report, indent=2))
