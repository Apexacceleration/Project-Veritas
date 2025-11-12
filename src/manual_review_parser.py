"""
Project Veritas - Manual Review Parser
Parses manually pasted Amazon reviews into structured format
"""

from typing import List, Dict
from datetime import datetime
import re


def parse_manual_reviews(text: str) -> List[Dict]:
    """
    Parse manually pasted Amazon reviews into structured format.

    Accepts various formats:
    - Full review text with rating/date/author
    - Just review text (will infer rating from content)
    - Multiple reviews separated by blank lines

    Returns:
        List[Dict]: List of review dictionaries in standard format
    """
    if not text or not text.strip():
        return []

    reviews = []

    # Split by double newlines (blank lines) to separate reviews
    review_blocks = re.split(r'\n\s*\n', text.strip())

    for i, block in enumerate(review_blocks):
        if not block.strip():
            continue

        review = parse_single_review(block, review_number=i + 1)
        if review:
            reviews.append(review)

    return reviews


def parse_single_review(text: str, review_number: int = 1) -> Dict:
    """
    Parse a single review block into structured format.

    Tries to extract:
    - Rating (from text like "5.0 out of 5 stars" or "⭐⭐⭐⭐⭐")
    - Date (from text like "Reviewed on January 15, 2024")
    - Author name
    - Review text

    Returns:
        Dict: Structured review data
    """
    if not text.strip():
        return None

    lines = text.strip().split('\n')

    # Initialize review dict with defaults
    review = {
        "rating": None,
        "title": "",
        "review_text": "",
        "date": None,
        "date_raw": "",
        "author": "Anonymous",
        "verified_purchase": False,
        "has_images": False,
        "review_length": 0
    }

    # Try to extract rating
    rating_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:out of 5|stars?|\/5)', text, re.IGNORECASE)
    if rating_match:
        review["rating"] = float(rating_match.group(1))
    else:
        # Try to count star symbols
        star_count = text.count('⭐') or text.count('★')
        if star_count > 0:
            review["rating"] = float(min(star_count, 5))

    # Try to extract date
    date_patterns = [
        r'(?:reviewed|posted|on)\s+([A-Z][a-z]+ \d{1,2},? \d{4})',
        r'(\d{1,2}/\d{1,2}/\d{2,4})',
        r'([A-Z][a-z]+ \d{1,2},? \d{4})'
    ]

    for pattern in date_patterns:
        date_match = re.search(pattern, text, re.IGNORECASE)
        if date_match:
            review["date_raw"] = date_match.group(1)
            try:
                from dateutil import parser
                review["date"] = parser.parse(date_match.group(1))
            except:
                pass
            break

    # Try to extract author
    author_patterns = [
        r'(?:by|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+(?:\s+[A-Z]\.?)?)\s+reviewed'
    ]

    for pattern in author_patterns:
        author_match = re.search(pattern, text)
        if author_match:
            review["author"] = author_match.group(1).strip()
            break

    # Check for verified purchase
    if 'verified purchase' in text.lower():
        review["verified_purchase"] = True

    # Extract review text (the main content)
    # Remove metadata lines and keep the actual review content
    review_lines = []
    for line in lines:
        line_clean = line.strip()

        # Skip metadata lines
        if any(keyword in line_clean.lower() for keyword in [
            'out of 5 stars',
            'reviewed on',
            'verified purchase',
            'helpful',
            'report'
        ]):
            # But check if it's part of the review text
            if len(line_clean) > 50:  # Likely review text that mentions these words
                review_lines.append(line_clean)
            continue

        if line_clean:
            review_lines.append(line_clean)

    # First line might be title if it's short
    if review_lines and len(review_lines[0]) < 100:
        review["title"] = review_lines[0]
        review["review_text"] = '\n'.join(review_lines[1:]) if len(review_lines) > 1 else review_lines[0]
    else:
        review["review_text"] = '\n'.join(review_lines)

    # If no rating found, try to infer from sentiment
    if review["rating"] is None:
        review["rating"] = infer_rating_from_text(review["review_text"])

    # Calculate review length
    full_text = review["title"] + " " + review["review_text"]
    review["review_length"] = len(full_text.strip())

    # Only return if we have review text
    if not review["review_text"].strip():
        return None

    return review


def infer_rating_from_text(text: str) -> float:
    """
    Infer rating from review text based on sentiment keywords.

    Returns rating between 1.0 and 5.0 (defaults to 3.0 if unclear)
    """
    text_lower = text.lower()

    # Positive keywords
    positive_words = ['amazing', 'excellent', 'perfect', 'love', 'great', 'awesome',
                      'wonderful', 'fantastic', 'best', 'incredible', 'outstanding']

    # Negative keywords
    negative_words = ['terrible', 'awful', 'horrible', 'worst', 'hate', 'garbage',
                      'useless', 'waste', 'disappointed', 'poor', 'bad']

    # Count occurrences
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    # Determine rating
    if positive_count > negative_count and positive_count >= 2:
        return 5.0
    elif positive_count > negative_count:
        return 4.0
    elif negative_count > positive_count and negative_count >= 2:
        return 1.0
    elif negative_count > positive_count:
        return 2.0
    else:
        return 3.0  # Neutral/unclear


def format_reviews_for_analysis(reviews: List[Dict]) -> List[Dict]:
    """
    Ensure manually parsed reviews match the expected format for analysis.

    Returns:
        List[Dict]: Reviews in standard format
    """
    formatted = []

    for review in reviews:
        # Ensure all required fields exist
        formatted_review = {
            "rating": review.get("rating", 3.0),
            "title": review.get("title", ""),
            "review_text": review.get("review_text", ""),
            "date": review.get("date"),
            "date_raw": review.get("date_raw", ""),
            "author": review.get("author", "Anonymous"),
            "verified_purchase": review.get("verified_purchase", False),
            "has_images": review.get("has_images", False),
            "review_length": review.get("review_length", len(review.get("review_text", "")))
        }

        formatted.append(formatted_review)

    return formatted
