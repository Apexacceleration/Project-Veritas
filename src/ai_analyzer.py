"""
Project Veritas - AI-Enhanced Analysis Module
Uses OpenAI GPT-5 for advanced linguistic analysis and authenticity detection

GPT-5 Benefits for Fake Review Detection:
- 45% fewer hallucinations than GPT-4o (more reliable results)
- 74.9% on SWE-bench (superior reasoning)
- Adaptive reasoning levels (automatically adjusts complexity)
- Better at detecting subtle linguistic deception
"""

import sys
import os
from typing import List, Dict, Optional
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

# OpenAI import (will be optional if not configured)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI library not installed. Run: pip install openai")


class AIReviewAnalyzer:
    """
    AI-enhanced review analyzer using OpenAI's GPT-5 models.

    Uses GPT-5-mini by default for optimal cost/performance balance:
    - More accurate than GPT-4o-mini
    - 45% fewer hallucinations = more reliable fake detection
    - Adaptive reasoning (automatically scales complexity)
    - Excellent for linguistic deception detection
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer with GPT-5.

        Args:
            api_key (str, optional): OpenAI API key. If None, reads from env/config.
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Run: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = OpenAI(api_key=self.api_key)

        # Check for model override from web interface (environment variable)
        # Priority: 1) env var (from web UI), 2) config.py default
        self.model = os.getenv("VERITAS_AI_MODEL") or getattr(config, "OPENAI_MODEL", "gpt-5-mini")

        print(f"🤖 Using AI model: {self.model}")

    def analyze_single_review(self, review: Dict) -> Dict:
        """
        Analyzes a single review for authenticity using AI.

        Args:
            review (Dict): Review dictionary with 'review_text', 'rating', etc.

        Returns:
            Dict: {
                "authenticity_score": float (0-100, higher = more authentic),
                "confidence": float (0-1),
                "reasoning": str,
                "red_flags": List[str],
                "is_suspicious": bool
            }
        """
        review_text = review.get("review_text", "")
        rating = review.get("rating", 0)
        verified = review.get("verified_purchase", False)

        if not review_text:
            return {
                "authenticity_score": 50,
                "confidence": 0,
                "reasoning": "No review text to analyze",
                "red_flags": [],
                "is_suspicious": False
            }

        prompt = self._build_single_review_prompt(review_text, rating, verified)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at detecting fake, incentivized, or manipulated online reviews. Analyze reviews for authenticity based on linguistic patterns, sentiment coherence, and deceptive indicators."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"⚠️  AI analysis error: {e}")
            return {
                "authenticity_score": 50,
                "confidence": 0,
                "reasoning": f"Analysis failed: {str(e)}",
                "red_flags": [],
                "is_suspicious": False
            }

    def analyze_review_batch(self, reviews: List[Dict], sample_size: int = 20) -> Dict:
        """
        Analyzes a batch of reviews to detect overall manipulation patterns.

        Args:
            reviews (List[Dict]): List of review dictionaries
            sample_size (int): Number of reviews to analyze (for cost control)

        Returns:
            Dict: {
                "overall_authenticity": float (0-100),
                "manipulation_likelihood": str ("low", "medium", "high"),
                "patterns_detected": List[str],
                "sample_size": int,
                "reasoning": str
            }
        """
        # Sample reviews for cost efficiency
        import random
        sampled_reviews = random.sample(reviews, min(sample_size, len(reviews)))

        # Build summary of reviews for batch analysis
        review_summaries = []
        for i, review in enumerate(sampled_reviews[:10], 1):  # Limit to 10 for token efficiency
            review_summaries.append(f"Review {i}: {review.get('rating', '?')}⭐ - {review.get('review_text', '')[:200]}")

        prompt = self._build_batch_analysis_prompt(review_summaries, len(reviews))

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at detecting coordinated fake review campaigns and manipulation patterns across multiple reviews."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            result["sample_size"] = len(sampled_reviews)
            return result

        except Exception as e:
            print(f"⚠️  Batch AI analysis error: {e}")
            return {
                "overall_authenticity": 50,
                "manipulation_likelihood": "unknown",
                "patterns_detected": [],
                "sample_size": 0,
                "reasoning": f"Analysis failed: {str(e)}"
            }

    def _build_single_review_prompt(self, review_text: str, rating: float, verified: bool) -> str:
        """Builds prompt for single review analysis."""
        return f"""Analyze this product review for authenticity.

Review Text: "{review_text}"
Star Rating: {rating}/5
Verified Purchase: {verified}

Evaluate based on:
1. Linguistic naturalness (does it sound human and genuine?)
2. Specificity (does it mention concrete details about the product?)
3. Sentiment-rating coherence (does the text match the star rating?)
4. Red flags (generic praise, keyword stuffing, promotional language, etc.)

Respond in JSON format:
{{
    "authenticity_score": <0-100, where 100 is definitely authentic>,
    "confidence": <0.0-1.0, your confidence in this assessment>,
    "reasoning": "<brief 1-2 sentence explanation>",
    "red_flags": ["<list of specific issues found>"],
    "is_suspicious": <true/false>
}}"""

    def _build_batch_analysis_prompt(self, review_summaries: List[str], total_count: int) -> str:
        """Builds prompt for batch review analysis."""
        reviews_text = "\n".join(review_summaries)

        return f"""Analyze this sample of product reviews ({len(review_summaries)} shown, {total_count} total) for patterns of manipulation or fake reviews.

{reviews_text}

Look for:
1. Repetitive language or phrasing across reviews
2. Suspiciously uniform sentiment
3. Generic praise without specific details
4. Signs of coordinated campaigns
5. Unnatural language patterns

Respond in JSON format:
{{
    "overall_authenticity": <0-100, where 100 is highly authentic dataset>,
    "manipulation_likelihood": "<low/medium/high>",
    "patterns_detected": ["<list of suspicious patterns found>"],
    "reasoning": "<2-3 sentence explanation of your assessment>"
}}"""


def enhance_analysis_with_ai(reviews: List[Dict], analysis_report: Dict, api_key: Optional[str] = None) -> Dict:
    """
    Enhances the statistical analysis with AI-powered insights.

    Args:
        reviews (List[Dict]): All reviews
        analysis_report (Dict): Existing analysis from analyzer.py
        api_key (str, optional): OpenAI API key

    Returns:
        Dict: Enhanced analysis report with AI insights
    """
    print("\n🤖 Enhancing analysis with AI...")

    if not OPENAI_AVAILABLE:
        print("   ⚠️  OpenAI not available, skipping AI analysis")
        return analysis_report

    try:
        ai_analyzer = AIReviewAnalyzer(api_key=api_key)

        # Perform batch analysis
        ai_batch_result = ai_analyzer.analyze_review_batch(reviews, sample_size=20)

        # Add AI insights to report
        analysis_report["ai_insights"] = {
            "overall_authenticity": ai_batch_result.get("overall_authenticity", 50),
            "manipulation_likelihood": ai_batch_result.get("manipulation_likelihood", "unknown"),
            "patterns_detected": ai_batch_result.get("patterns_detected", []),
            "reasoning": ai_batch_result.get("reasoning", ""),
            "sample_size": ai_batch_result.get("sample_size", 0)
        }

        # Adjust trust score based on AI insights
        ai_score = ai_batch_result.get("overall_authenticity", 50)

        # If AI detects major issues, add penalty
        if ai_batch_result.get("manipulation_likelihood") == "high":
            analysis_report["total_score_impact"] -= 10
            analysis_report["triggered_flags"].append("ai_detected_manipulation")
            print(f"   ⚠️  AI detected high manipulation likelihood")

        print(f"   ✓ AI Analysis: {ai_score:.1f}/100 authenticity")
        print(f"   ✓ Manipulation risk: {ai_batch_result.get('manipulation_likelihood', 'unknown').upper()}")

    except Exception as e:
        print(f"   ⚠️  Could not perform AI analysis: {e}")
        analysis_report["ai_insights"] = {
            "error": str(e),
            "overall_authenticity": None
        }

    return analysis_report


# Example usage
if __name__ == "__main__":
    # Test AI analyzer (requires OPENAI_API_KEY in environment)
    test_review = {
        "review_text": "This product is amazing! Great quality! Highly recommend! Best purchase ever!",
        "rating": 5.0,
        "verified_purchase": False
    }

    try:
        analyzer = AIReviewAnalyzer()
        result = analyzer.analyze_single_review(test_review)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set OPENAI_API_KEY environment variable")
