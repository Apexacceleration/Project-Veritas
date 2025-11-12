"""
Project Veritas - Utility Functions
Helper functions for scraping, text processing, and general utilities
"""

import random
import time
import re
from datetime import datetime
from typing import List, Dict
import config


def get_random_user_agent() -> str:
    """
    Returns a random user agent string from the config to simulate different browsers.
    Helps avoid detection by anti-scraping systems.

    Returns:
        str: Random user agent string
    """
    return random.choice(config.USER_AGENTS)


def random_delay(min_delay: float = None, max_delay: float = None) -> None:
    """
    Introduces a random delay to simulate human browsing behavior.
    Helps avoid triggering rate limits or bot detection.

    Args:
        min_delay (float, optional): Minimum delay in seconds. Defaults to config value.
        max_delay (float, optional): Maximum delay in seconds. Defaults to config value.
    """
    min_d = min_delay or config.REQUEST_MIN_DELAY
    max_d = max_delay or config.REQUEST_MAX_DELAY
    delay = random.uniform(min_d, max_d)
    time.sleep(delay)


def parse_amazon_date(date_string: str) -> datetime:
    """
    Parses various Amazon date formats into a datetime object.
    Amazon uses formats like "Reviewed in the United States on January 15, 2024"

    Args:
        date_string (str): The date string from Amazon review

    Returns:
        datetime: Parsed datetime object, or None if parsing fails
    """
    try:
        # Extract the actual date part (after "on")
        if " on " in date_string:
            date_string = date_string.split(" on ")[-1]

        # Try different date formats
        date_formats = [
            "%B %d, %Y",      # January 15, 2024
            "%b %d, %Y",       # Jan 15, 2024
            "%Y-%m-%d",        # 2024-01-15
            "%m/%d/%Y",        # 01/15/2024
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_string.strip(), fmt)
            except ValueError:
                continue

        return None
    except Exception:
        return None


def clean_text(text: str) -> str:
    """
    Cleans and normalizes review text for analysis.
    Removes extra whitespace, special characters, etc.

    Args:
        text (str): Raw text to clean

    Returns:
        str: Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def extract_rating_number(rating_string: str) -> float:
    """
    Extracts numeric rating from Amazon rating string.
    Examples: "5.0 out of 5 stars" -> 5.0, "4 stars" -> 4.0

    Args:
        rating_string (str): Rating string from Amazon

    Returns:
        float: Numeric rating (1.0-5.0), or None if parsing fails
    """
    try:
        # Look for number followed by "out of" or "stars"
        match = re.search(r'(\d+\.?\d*)\s*(?:out of|stars?)', rating_string)
        if match:
            return float(match.group(1))

        # Try to extract any number
        match = re.search(r'(\d+\.?\d*)', rating_string)
        if match:
            rating = float(match.group(1))
            # Ensure it's in valid range
            if 1.0 <= rating <= 5.0:
                return rating

        return None
    except Exception:
        return None


def is_verified_purchase(text: str) -> bool:
    """
    Checks if review has "Verified Purchase" badge.

    Args:
        text (str): Text that might contain verified purchase indicator

    Returns:
        bool: True if verified purchase, False otherwise
    """
    if not text:
        return False
    return "verified purchase" in text.lower()


def calculate_grade(score: float) -> str:
    """
    Converts a numeric score (0-100) to a letter grade (A-F).
    Uses the grading scale from config.py

    Args:
        score (float): Numeric score (0-100)

    Returns:
        str: Letter grade (A, B, C, D, or F)
    """
    # Ensure score is within bounds
    score = max(0, min(100, score))

    # Iterate through grade scale (sorted in descending order)
    for threshold in sorted(config.GRADE_SCALE.keys(), reverse=True):
        if score >= threshold:
            return config.GRADE_SCALE[threshold]

    return "F"  # Fallback


def get_ngrams(text: str, n: int = 4) -> List[str]:
    """
    Extracts n-grams (sequences of n words) from text.
    Used for detecting repetitive phrases across reviews.

    Args:
        text (str): Text to extract n-grams from
        n (int): Number of words in each n-gram (default: 4)

    Returns:
        List[str]: List of n-gram strings
    """
    words = text.lower().split()
    if len(words) < n:
        return []

    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = " ".join(words[i:i+n])
        ngrams.append(ngram)

    return ngrams


def format_percentage(value: float) -> str:
    """
    Formats a decimal as a percentage string.

    Args:
        value (float): Decimal value (e.g., 0.75)

    Returns:
        str: Formatted percentage (e.g., "75%")
    """
    return f"{value * 100:.1f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divides two numbers, returning default if denominator is 0.

    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default (float): Value to return if division by zero (default: 0.0)

    Returns:
        float: Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator
