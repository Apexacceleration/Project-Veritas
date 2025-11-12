"""
Project Veritas - Web Scraper Module
Scrapes Amazon product reviews with anti-scraping resilience measures
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import re
import sys
import os

# Add parent directory to path to import config and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src import utils


class AmazonReviewScraper:
    """
    Scraper for Amazon product reviews with built-in anti-bot measures.
    """

    def __init__(self):
        self.session = requests.Session()
        self.reviews = []

    def _get_headers(self) -> Dict[str, str]:
        """
        Generates request headers with rotating user agent.

        Returns:
            Dict[str, str]: HTTP headers
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

    def _extract_product_id(self, url: str) -> Optional[str]:
        """
        Extracts Amazon product ASIN from URL.
        Examples:
        - amazon.com/dp/B08N5WRWNW -> B08N5WRWNW
        - amazon.com/product/B08N5WRWNW -> B08N5WRWNW

        Args:
            url (str): Amazon product URL

        Returns:
            Optional[str]: ASIN product ID, or None if not found
        """
        # Match ASIN pattern (usually 10 alphanumeric characters)
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

    def _build_review_url(self, asin: str, page: int = 1) -> str:
        """
        Constructs the URL for Amazon review pages.

        Args:
            asin (str): Amazon product ASIN
            page (int): Page number (default: 1)

        Returns:
            str: Review page URL
        """
        base_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page}"
        params = {
            "pageNumber": page,
            "sortBy": "recent"  # Sort by most recent reviews
        }

        # Build query string
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"

    def _parse_review_element(self, review_element) -> Optional[Dict]:
        """
        Parses a single review HTML element into a structured dictionary.

        Args:
            review_element: BeautifulSoup element containing review data

        Returns:
            Optional[Dict]: Parsed review data, or None if parsing fails
        """
        try:
            review_data = {}

            # Extract rating (e.g., "5.0 out of 5 stars")
            rating_elem = review_element.find("i", {"data-hook": "review-star-rating"})
            if rating_elem:
                rating_text = rating_elem.get_text()
                review_data["rating"] = utils.extract_rating_number(rating_text)
            else:
                review_data["rating"] = None

            # Extract review title
            title_elem = review_element.find("a", {"data-hook": "review-title"})
            if title_elem:
                review_data["title"] = utils.clean_text(title_elem.get_text())
            else:
                review_data["title"] = ""

            # Extract review body text
            body_elem = review_element.find("span", {"data-hook": "review-body"})
            if body_elem:
                review_data["review_text"] = utils.clean_text(body_elem.get_text())
            else:
                review_data["review_text"] = ""

            # Extract review date
            date_elem = review_element.find("span", {"data-hook": "review-date"})
            if date_elem:
                date_text = date_elem.get_text()
                review_data["date"] = utils.parse_amazon_date(date_text)
                review_data["date_raw"] = date_text
            else:
                review_data["date"] = None
                review_data["date_raw"] = ""

            # Extract reviewer name/profile
            author_elem = review_element.find("span", class_="a-profile-name")
            if author_elem:
                review_data["author"] = utils.clean_text(author_elem.get_text())
            else:
                review_data["author"] = "Anonymous"

            # Check for verified purchase badge
            verified_elem = review_element.find("span", {"data-hook": "avp-badge"})
            review_data["verified_purchase"] = verified_elem is not None

            # Check for customer images
            image_elem = review_element.find("img", class_="review-image-tile")
            review_data["has_images"] = image_elem is not None

            # Calculate review length
            full_text = review_data["title"] + " " + review_data["review_text"]
            review_data["review_length"] = len(full_text)

            # Only return if we have essential data
            if review_data["review_text"] and review_data["rating"]:
                return review_data
            else:
                return None

        except Exception as e:
            print(f"Warning: Failed to parse review element: {e}")
            return None

    def scrape_reviews(self, url: str, max_pages: int = 10) -> List[Dict]:
        """
        Main scraping function. Scrapes reviews from Amazon product URL.

        Args:
            url (str): Amazon product URL
            max_pages (int): Maximum number of review pages to scrape (default: 10)

        Returns:
            List[Dict]: List of parsed review dictionaries

        Example return structure:
        [
            {
                "rating": 5.0,
                "title": "Great product!",
                "review_text": "This camera is amazing...",
                "date": datetime(2024, 1, 15),
                "date_raw": "Reviewed in the United States on January 15, 2024",
                "author": "John Doe",
                "verified_purchase": True,
                "has_images": True,
                "review_length": 150
            },
            ...
        ]
        """
        print(f"🔍 Starting scrape for: {url}")

        # Extract product ASIN
        asin = self._extract_product_id(url)
        if not asin:
            raise ValueError(f"Could not extract product ID from URL: {url}")

        print(f"📦 Product ASIN: {asin}")

        self.reviews = []
        reviews_scraped = 0

        # Scrape multiple pages
        for page in range(1, max_pages + 1):
            # Check if we've hit the maximum review limit
            if reviews_scraped >= config.MAX_REVIEWS_TO_SCRAPE:
                print(f"✅ Reached maximum review limit ({config.MAX_REVIEWS_TO_SCRAPE})")
                break

            print(f"📄 Scraping page {page}...")

            # Build review page URL
            review_url = self._build_review_url(asin, page)

            try:
                # Random delay to simulate human behavior
                if page > 1:
                    utils.random_delay()

                # Make request
                response = self.session.get(
                    review_url,
                    headers=self._get_headers(),
                    timeout=config.REQUEST_TIMEOUT
                )

                # Check if request was successful
                if response.status_code != 200:
                    print(f"⚠️  Warning: Got status code {response.status_code} on page {page}")
                    # If blocked, stop scraping
                    if response.status_code == 503:
                        print("🚫 Amazon has blocked our requests. Consider using proxies or reducing request rate.")
                        break
                    continue

                # Parse HTML
                soup = BeautifulSoup(response.content, "lxml")

                # Debug: Check if we're being blocked
                if "To discuss automated access to Amazon data please contact" in response.text:
                    print("🚫 Amazon bot detection triggered. Try again later or use proxies.")
                    break

                # Find all review elements
                review_elements = soup.find_all("div", {"data-hook": "review"})

                # Debug: If no reviews found, check page content
                if not review_elements:
                    print(f"ℹ️  No reviews found on page {page}.")
                    # Check if page has any review-related content
                    if page == 1:
                        print(f"   Debug: Page title: {soup.title.string if soup.title else 'No title'}")
                        print(f"   Debug: Response length: {len(response.text)} characters")
                    break

                # Parse each review
                page_reviews = 0
                for elem in review_elements:
                    review = self._parse_review_element(elem)
                    if review:
                        self.reviews.append(review)
                        reviews_scraped += 1
                        page_reviews += 1

                        # Check limit
                        if reviews_scraped >= config.MAX_REVIEWS_TO_SCRAPE:
                            break

                print(f"   ✓ Scraped {page_reviews} reviews from page {page}")

            except requests.exceptions.Timeout:
                print(f"⚠️  Timeout on page {page}. Skipping.")
                continue
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Request error on page {page}: {e}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error on page {page}: {e}")
                continue

        print(f"\n✅ Scraping complete! Total reviews: {len(self.reviews)}")
        return self.reviews


def scrape_reviews(url: str) -> List[Dict]:
    """
    Convenience function to scrape reviews from an Amazon product URL.

    Args:
        url (str): Amazon product URL

    Returns:
        List[Dict]: List of review dictionaries
    """
    scraper = AmazonReviewScraper()
    return scraper.scrape_reviews(url)


# Example usage (for testing)
if __name__ == "__main__":
    # Test with a sample Amazon URL
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"  # Example ASIN
    reviews = scrape_reviews(test_url)

    print(f"\n📊 Sample review:")
    if reviews:
        print(reviews[0])
