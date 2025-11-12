"""
Project Veritas - RapidAPI Amazon Review Scraper
Uses RapidAPI to fetch Amazon reviews (with free tier support)
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime


class RapidAPIAmazonScraper:
    """
    Scraper using RapidAPI for Amazon reviews.
    Falls back gracefully when rate limits are hit.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.base_url = "https://real-time-amazon-data.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
        }

    def _extract_asin(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon URL."""
        import re
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'[?&]asin=([A-Z0-9]{10})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def scrape_reviews(self, url: str, max_reviews: int = 100) -> Dict:
        """
        Scrape reviews using RapidAPI.

        Returns:
            Dict with 'success', 'reviews', and 'error' keys
        """
        if not self.api_key or self.api_key == "your-rapidapi-key-here":
            return {
                "success": False,
                "error": "RapidAPI key not configured",
                "reviews": [],
                "rate_limited": False
            }

        asin = self._extract_asin(url)
        if not asin:
            return {
                "success": False,
                "error": f"Could not extract ASIN from URL: {url}",
                "reviews": [],
                "rate_limited": False
            }

        print(f"🔍 Fetching reviews via RapidAPI for ASIN: {asin}")

        try:
            # Call RapidAPI product reviews endpoint
            endpoint = f"{self.base_url}/product-reviews"
            params = {
                "asin": asin,
                "country": "US",
                "page": "1"
            }

            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )

            # Check for rate limiting
            if response.status_code == 429:
                print("⚠️ RapidAPI rate limit reached (free tier exhausted)")
                return {
                    "success": False,
                    "error": "Rate limit exceeded - free tier exhausted for this month",
                    "reviews": [],
                    "rate_limited": True
                }

            # Check for API key issues
            if response.status_code == 403:
                print("⚠️ RapidAPI authentication failed")
                return {
                    "success": False,
                    "error": "API authentication failed - check your RapidAPI key",
                    "reviews": [],
                    "rate_limited": False
                }

            # Check for success
            if response.status_code != 200:
                print(f"⚠️ RapidAPI returned status code: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API returned status code {response.status_code}",
                    "reviews": [],
                    "rate_limited": False
                }

            # Parse response
            data = response.json()

            # Extract reviews from response
            reviews = self._parse_rapidapi_response(data)

            if not reviews:
                return {
                    "success": False,
                    "error": "No reviews found in API response",
                    "reviews": [],
                    "rate_limited": False
                }

            print(f"✅ Successfully fetched {len(reviews)} reviews via RapidAPI")

            return {
                "success": True,
                "reviews": reviews[:max_reviews],
                "error": None,
                "rate_limited": False
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "API request timed out",
                "reviews": [],
                "rate_limited": False
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "reviews": [],
                "rate_limited": False
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "reviews": [],
                "rate_limited": False
            }

    def _parse_rapidapi_response(self, data: Dict) -> List[Dict]:
        """
        Parse RapidAPI response into our standard review format.

        Note: This format may need adjustment based on actual API response.
        """
        reviews = []

        # RapidAPI response format varies by endpoint
        # Common patterns: data['reviews'], data['data']['reviews'], data['results']
        review_list = (
            data.get('data', {}).get('reviews', []) or
            data.get('reviews', []) or
            data.get('results', [])
        )

        for review_data in review_list:
            try:
                review = {
                    "rating": self._extract_rating(review_data),
                    "title": review_data.get('title', ''),
                    "review_text": review_data.get('body', '') or review_data.get('text', ''),
                    "date": self._parse_date(review_data.get('date', '')),
                    "date_raw": review_data.get('date', ''),
                    "author": review_data.get('author', {}).get('name', 'Anonymous'),
                    "verified_purchase": review_data.get('verified_purchase', False),
                    "has_images": bool(review_data.get('images', [])),
                    "review_length": len(review_data.get('body', '') or review_data.get('text', ''))
                }

                # Only add if we have essential data
                if review["review_text"] and review["rating"]:
                    reviews.append(review)

            except Exception as e:
                print(f"Warning: Failed to parse review: {e}")
                continue

        return reviews

    def _extract_rating(self, review_data: Dict) -> Optional[float]:
        """Extract rating from various possible formats."""
        rating = review_data.get('rating') or review_data.get('stars')

        if rating is None:
            return None

        # Handle string ratings like "5.0 out of 5 stars"
        if isinstance(rating, str):
            import re
            match = re.search(r'(\d+\.?\d*)', rating)
            if match:
                return float(match.group(1))

        return float(rating)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        try:
            # Try common date formats
            from dateutil import parser
            return parser.parse(date_str)
        except:
            return None


def scrape_reviews_rapidapi(url: str, api_key: Optional[str] = None) -> Dict:
    """
    Convenience function to scrape reviews using RapidAPI.

    Returns:
        Dict with 'success', 'reviews', 'error', and 'rate_limited' keys
    """
    scraper = RapidAPIAmazonScraper(api_key)
    return scraper.scrape_reviews(url)
