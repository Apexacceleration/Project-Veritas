"""
Project Veritas - Multi-API RapidAPI Scraper
Rotates between multiple RapidAPI keys/services when rate limited
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime
import re


class MultiAPIAmazonScraper:
    """
    Scraper that rotates between multiple RapidAPI keys/services.
    Automatically tries next API when one is rate limited.
    """

    def __init__(self, api_keys: Optional[List[str]] = None):
        # Load API keys (supports multiple keys)
        if api_keys:
            self.api_keys = api_keys
        else:
            # Try to load from Streamlit secrets or environment
            # Format: RAPIDAPI_KEY_1, RAPIDAPI_KEY_2, etc.
            self.api_keys = []

            # Try Streamlit secrets first (for deployed apps)
            try:
                import streamlit as st
                # Check if secrets are available
                if hasattr(st, 'secrets'):
                    print(f"   Debug: st.secrets is available")
                    print(f"   Debug: Available secret keys: {list(st.secrets.keys())}")

                    for i in range(1, 11):  # Support up to 10 API keys
                        try:
                            key_name = f"RAPIDAPI_KEY_{i}"
                            if key_name in st.secrets:
                                key = st.secrets[key_name]
                                if key and key != "your-key-here":
                                    self.api_keys.append(key)
                                    print(f"   Debug: Loaded {key_name}")
                        except Exception as e:
                            print(f"   Debug: Failed to load {key_name}: {e}")
                            pass

                    # Fallback to single key if no numbered keys found
                    if not self.api_keys:
                        try:
                            if "RAPIDAPI_KEY" in st.secrets:
                                single_key = st.secrets["RAPIDAPI_KEY"]
                                if single_key and single_key != "your-key-here":
                                    self.api_keys = [single_key]
                                    print(f"   Debug: Loaded RAPIDAPI_KEY")
                        except Exception as e:
                            print(f"   Debug: Failed to load RAPIDAPI_KEY: {e}")
                            pass
                else:
                    print(f"   Debug: st.secrets not available")
            except ImportError:
                # Not in Streamlit, use environment variables
                print(f"   Debug: Streamlit not imported")
                pass
            except Exception as e:
                print(f"   Debug: Error accessing Streamlit secrets: {e}")

            # If still no keys, try environment variables
            if not self.api_keys:
                for i in range(1, 11):
                    key = os.getenv(f"RAPIDAPI_KEY_{i}", "")
                    if key and key != "your-key-here":
                        self.api_keys.append(key)

                # Fallback to single key
                if not self.api_keys:
                    single_key = os.getenv("RAPIDAPI_KEY", "")
                    if single_key and single_key != "your-key-here":
                        self.api_keys = [single_key]

        print(f"🔑 Loaded {len(self.api_keys)} RapidAPI key(s)")
        if self.api_keys:
            print(f"   First key preview: {self.api_keys[0][:20]}...")
        else:
            print("   ⚠️ WARNING: No API keys found!")

        # Multiple API service configurations (rotate through these too)
        # Currently only using OpenWeb Ninja since all accounts are subscribed to it
        self.api_services = [
            {
                "name": "Real-Time Amazon Data (OpenWeb Ninja)",
                "base_url": "https://real-time-amazon-data.p.rapidapi.com",
                "host": "real-time-amazon-data.p.rapidapi.com",
                "product_endpoint": "/product-details",
                "reviews_endpoint": "/product-reviews"
            }
            # Uncomment these if you subscribe to other APIs:
            # {
            #     "name": "Realtime Amazon Data (API World)",
            #     "base_url": "https://realtime-amazon-data.p.rapidapi.com",
            #     "host": "realtime-amazon-data.p.rapidapi.com",
            #     "product_endpoint": "/product-details",
            #     "reviews_endpoint": "/product-reviews"
            # },
            # {
            #     "name": "Scout Amazon Data",
            #     "base_url": "https://scout-amazon-data.p.rapidapi.com",
            #     "host": "scout-amazon-data.p.rapidapi.com",
            #     "product_endpoint": "/product-details",
            #     "reviews_endpoint": "/product-reviews"
            # }
        ]

    def _extract_asin(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon URL."""
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
        Scrape reviews using RapidAPI with automatic key rotation.

        Returns:
            Dict with 'success', 'reviews', 'error', and 'rate_limited' keys
        """
        if not self.api_keys:
            return {
                "success": False,
                "error": "No RapidAPI keys configured",
                "reviews": [],
                "rate_limited": False,
                "all_apis_exhausted": False
            }

        asin = self._extract_asin(url)
        if not asin:
            return {
                "success": False,
                "error": f"Could not extract ASIN from URL: {url}",
                "reviews": [],
                "rate_limited": False,
                "all_apis_exhausted": False
            }

        print(f"🔍 Fetching reviews for ASIN: {asin}")

        # Try each API key in sequence until one works
        for i, api_key in enumerate(self.api_keys, 1):
            print(f"🚀 Trying API key #{i}...")

            # Try each API service with this key
            for service in self.api_services:
                print(f"   📡 Trying {service['name']}...")
                result = self._try_api_key(api_key, asin, max_reviews, service)

                if result["success"]:
                    print(f"✅ Success with API key #{i} using {service['name']}!")
                    return result
                elif result["rate_limited"]:
                    print(f"   ⚠️ Rate limited on {service['name']}, trying next service...")
                    continue
                else:
                    # Other error (auth failure, network issue, etc.)
                    print(f"   ⚠️ Error on {service['name']}: {result['error']}")
                    # Try next service with this key
                    continue

            print(f"⚠️ API key #{i} exhausted all services, trying next key...")

        # All API keys and services are exhausted
        print("❌ All API keys and services are rate limited!")
        return {
            "success": False,
            "error": "All RapidAPI keys have reached their rate limits across all services",
            "reviews": [],
            "rate_limited": True,
            "all_apis_exhausted": True
        }

    def _try_api_key(self, api_key: str, asin: str, max_reviews: int, api_config: Dict) -> Dict:
        """
        Try to fetch reviews using a specific API key and service.
        Fetches multiple pages if needed to reach max_reviews.

        Returns:
            Dict with result of this attempt
        """
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_config["host"]
        }

        try:
            # First, get product details (includes some review info)
            product_url = f"{api_config['base_url']}{api_config['product_endpoint']}"
            product_params = {
                "asin": asin,
                "country": "US"
            }

            product_response = requests.get(
                product_url,
                headers=headers,
                params=product_params,
                timeout=30
            )

            # Check for rate limiting
            if product_response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "reviews": [],
                    "rate_limited": True
                }

            # Check for authentication issues
            if product_response.status_code == 403:
                return {
                    "success": False,
                    "error": "API authentication failed",
                    "reviews": [],
                    "rate_limited": False
                }

            # Check for other errors
            if product_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"API returned status code {product_response.status_code}",
                    "reviews": [],
                    "rate_limited": False
                }

            # Fetch reviews with pagination
            # Cost: 1 product call + up to 13 review pages = 14 API calls per product (worst case)
            # With 500 requests/month across 5 keys = ~35 product analyses per month
            all_reviews = []
            page = 1
            max_pages = 13  # ~8 reviews per page * 13 pages = ~100 reviews

            while len(all_reviews) < max_reviews and page <= max_pages:
                reviews_url = f"{api_config['base_url']}{api_config['reviews_endpoint']}"
                reviews_params = {
                    "asin": asin,
                    "country": "US",
                    "page": str(page)
                }

                print(f"      Fetching page {page}...")
                reviews_response = requests.get(
                    reviews_url,
                    headers=headers,
                    params=reviews_params,
                    timeout=30
                )

                # Check for rate limiting
                if reviews_response.status_code == 429:
                    print(f"      Rate limited at page {page}")
                    if all_reviews:
                        # Return what we have so far
                        break
                    return {
                        "success": False,
                        "error": "Rate limit exceeded",
                        "reviews": [],
                        "rate_limited": True
                    }

                if reviews_response.status_code != 200:
                    print(f"      Page {page} returned status {reviews_response.status_code}")
                    break

                # Parse reviews from this page
                reviews_data = reviews_response.json()
                page_reviews = self._parse_reviews_response(reviews_data)

                if not page_reviews:
                    print(f"      No more reviews found at page {page}")
                    break

                all_reviews.extend(page_reviews)
                print(f"      Got {len(page_reviews)} reviews (total: {len(all_reviews)})")
                page += 1

            if not all_reviews:
                # Try to parse product details for embedded reviews as fallback
                product_data = product_response.json()
                reviews = self._extract_reviews_from_product_data(product_data)

                if reviews:
                    return {
                        "success": True,
                        "reviews": reviews[:max_reviews],
                        "error": None,
                        "rate_limited": False
                    }

                return {
                    "success": False,
                    "error": "No reviews found in API response",
                    "reviews": [],
                    "rate_limited": False
                }

            return {
                "success": True,
                "reviews": all_reviews[:max_reviews],
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

    def _parse_reviews_response(self, data: Dict) -> List[Dict]:
        """Parse RapidAPI reviews response into standard format."""
        reviews = []

        # Try different response structures
        review_list = (
            data.get('data', {}).get('reviews', []) or
            data.get('reviews', []) or
            data.get('data', {}).get('results', []) or
            []
        )

        print(f"   Debug: Found {len(review_list)} reviews in response")
        if review_list:
            print(f"   Debug: First review keys: {list(review_list[0].keys())}")

        for review_data in review_list:
            try:
                rating = self._extract_rating(review_data)
                review_text = review_data.get('body', '') or review_data.get('review_comment', '') or review_data.get('text', '')

                # Extract author name
                author = review_data.get('review_author', '')
                if not author and isinstance(review_data.get('author'), dict):
                    author = review_data.get('author', {}).get('name', 'Anonymous')
                elif not author:
                    author = review_data.get('author', 'Anonymous')

                # Extract and parse date
                date_raw = review_data.get('date', '') or review_data.get('review_date', '')
                parsed_date = self._parse_date(date_raw)

                review = {
                    "rating": rating,
                    "title": review_data.get('title', '') or review_data.get('review_title', ''),
                    "review_text": review_text,
                    "date": parsed_date,
                    "date_raw": date_raw,
                    "author": author,
                    "verified_purchase": review_data.get('verified_purchase', False) or review_data.get('is_verified_purchase', False),
                    "has_images": bool(review_data.get('images', []) or review_data.get('review_images', [])),
                    "review_length": len(review_text)
                }

                # Debug: Show date parsing for first review
                if len(all_reviews) == 0:
                    print(f"      Debug: First review date_raw='{date_raw}', parsed={parsed_date}")

                # Debug why review might be rejected
                if not review_text:
                    print(f"   Debug: Review rejected - no text. Keys: {list(review_data.keys())}")
                if not rating:
                    print(f"   Debug: Review rejected - no rating. Available: {review_data.get('rating')}, {review_data.get('stars')}, {review_data.get('review_star')}")

                # Only add if we have essential data
                if review_text and rating:
                    reviews.append(review)

            except Exception as e:
                print(f"Warning: Failed to parse review: {e}")
                continue

        return reviews

    def _extract_reviews_from_product_data(self, product_data: Dict) -> List[Dict]:
        """Extract reviews from product details response (fallback)."""
        # Some APIs include top reviews in product details
        reviews = []
        top_reviews = product_data.get('data', {}).get('top_reviews', [])

        for review_data in top_reviews:
            try:
                review = {
                    "rating": self._extract_rating(review_data),
                    "title": review_data.get('title', ''),
                    "review_text": review_data.get('body', '') or review_data.get('text', ''),
                    "date": self._parse_date(review_data.get('date', '')),
                    "date_raw": review_data.get('date', ''),
                    "author": review_data.get('author', 'Anonymous'),
                    "verified_purchase": review_data.get('verified_purchase', False),
                    "has_images": bool(review_data.get('images', [])),
                    "review_length": len(review_data.get('body', '') or review_data.get('text', ''))
                }

                if review["review_text"] and review["rating"]:
                    reviews.append(review)

            except:
                continue

        return reviews

    def _extract_rating(self, review_data: Dict) -> Optional[float]:
        """Extract rating from various possible formats."""
        rating = (
            review_data.get('review_star_rating') or  # OpenWeb Ninja uses this
            review_data.get('rating') or
            review_data.get('stars') or
            review_data.get('review_star')
        )

        if rating is None:
            return None

        # Handle string ratings like "5.0 out of 5 stars"
        if isinstance(rating, str):
            match = re.search(r'(\d+\.?\d*)', rating)
            if match:
                return float(match.group(1))

        return float(rating)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        try:
            from dateutil import parser
            return parser.parse(date_str)
        except:
            return None


def scrape_reviews_multi_api(url: str, api_keys: Optional[List[str]] = None) -> Dict:
    """
    Convenience function to scrape reviews using multiple RapidAPI keys.

    Returns:
        Dict with 'success', 'reviews', 'error', 'rate_limited', and 'all_apis_exhausted' keys
    """
    scraper = MultiAPIAmazonScraper(api_keys)
    return scraper.scrape_reviews(url)
