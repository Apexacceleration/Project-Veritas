"""
Project Veritas - Review Analysis Tool
Finding truth in a world that wants to hide it—at least in online reviews.
"""

from src.main import run_veritas
from src.scraper import scrape_reviews
from src.analyzer import analyze_data
from src.scorer import generate_full_report

__version__ = "1.0.0"
__all__ = ["run_veritas", "scrape_reviews", "analyze_data", "generate_full_report"]
