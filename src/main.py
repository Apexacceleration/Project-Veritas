"""
Project Veritas - Main Application
Master orchestrator that ties together scraping, analysis, and scoring.
"""

import sys
import os
import json
from typing import Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.scraper import scrape_reviews
from src.analyzer import analyze_data
from src.scorer import generate_full_report


def run_veritas(url: str, output_file: str = None, verbose: bool = True) -> Dict:
    """
    Master function for Project Veritas.
    Scrapes reviews, analyzes for red flags, and generates Trust + Quality scores.

    Args:
        url (str): Amazon product URL to analyze
        output_file (str, optional): Path to save JSON report. If None, doesn't save.
        verbose (bool): Whether to print progress messages (default: True)

    Returns:
        Dict: Complete Veritas report with Trust and Quality scores

    Example:
        >>> report = run_veritas("https://amazon.com/dp/B08N5WRWNW")
        >>> print(f"Trust Score: {report['trust_score']}")
        >>> print(f"Quality Score: {report['quality_score']}")
    """

    if verbose:
        print("\n" + "="*60)
        print("🚀 PROJECT VERITAS - FINDING TRUTH IN REVIEWS")
        print("="*60)
        print(f"🔗 URL: {url}\n")

    try:
        # ====================================================================
        # STEP 1: SCRAPE REVIEWS
        # ====================================================================
        if verbose:
            print("📥 STEP 1: SCRAPING REVIEWS")
            print("-"*60)

        print(f"DEBUG: About to call scrape_reviews with URL: {url}")
        reviews = scrape_reviews(url)
        print(f"DEBUG: scrape_reviews returned {len(reviews) if reviews else 0} reviews")

        if reviews:
            # Debug: Check dates
            dates_parsed = sum(1 for r in reviews if r.get('date'))
            print(f"DEBUG: {dates_parsed}/{len(reviews)} reviews have parsed dates")
            if dates_parsed > 0:
                sample_review = next(r for r in reviews if r.get('date'))
                print(f"DEBUG: Sample date: {sample_review.get('date')} (from raw: {sample_review.get('date_raw')})")

        if not reviews:
            error_report = {
                "project": "Project Veritas",
                "url": url,
                "error": "No reviews found or unable to scrape",
                "trust_score": 0,
                "trust_grade": "F",
                "quality_score": 0,
                "quality_grade": "F",
                "total_reviews_analyzed": 0
            }
            return error_report

        if verbose:
            print(f"\n✅ Scraping complete: {len(reviews)} reviews collected\n")

        # ====================================================================
        # STEP 2: ANALYZE FOR RED FLAGS
        # ====================================================================
        if verbose:
            print("🔍 STEP 2: ANALYZING FOR RED FLAGS")
            print("-"*60)

        analysis_report = analyze_data(reviews)

        if verbose:
            print(f"\n✅ Analysis complete: {len(analysis_report['triggered_flags'])} red flags detected\n")

        # ====================================================================
        # STEP 3: CALCULATE SCORES AND GENERATE REPORT
        # ====================================================================
        if verbose:
            print("🎯 STEP 3: CALCULATING SCORES")
            print("-"*60)

        report = generate_full_report(reviews, analysis_report, url)

        # ====================================================================
        # STEP 4: SAVE TO FILE (OPTIONAL)
        # ====================================================================
        if output_file:
            if verbose:
                print(f"\n💾 STEP 4: SAVING REPORT")
                print("-"*60)

            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)

            if verbose:
                print(f"✅ Report saved to: {output_file}\n")

        # ====================================================================
        # DISPLAY RESULTS
        # ====================================================================
        if verbose:
            print_report_summary(report)

        return report

    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
        error_report = {
            "project": "Project Veritas",
            "url": url,
            "error": str(e),
            "trust_score": 0,
            "trust_grade": "F",
            "quality_score": 0,
            "quality_grade": "F",
            "total_reviews_analyzed": 0
        }
        return error_report

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        error_report = {
            "project": "Project Veritas",
            "url": url,
            "error": f"Unexpected error: {str(e)}",
            "trust_score": 0,
            "trust_grade": "F",
            "quality_score": 0,
            "quality_grade": "F",
            "total_reviews_analyzed": 0
        }
        return error_report


def print_report_summary(report: Dict) -> None:
    """
    Prints a nicely formatted summary of the Veritas report.

    Args:
        report (Dict): Veritas report dictionary
    """
    print("\n" + "="*60)
    print("📊 PROJECT VERITAS REPORT")
    print("="*60)
    print(f"🔗 Product URL: {report['url']}")
    print(f"📦 Total Reviews Analyzed: {report['total_reviews_analyzed']}")
    print(f"✅ Trusted Reviews: {report['trusted_reviews_count']}")
    print(f"⚠️  Suspicious Reviews: {report['suspicious_reviews_count']}")
    print()
    print("-"*60)
    print("🔒 TRUST SCORE (Review Reliability)")
    print("-"*60)
    print(f"   Score: {report['trust_score']} / 100")
    print(f"   Grade: {report['trust_grade']}")
    print(f"   Summary: {report['trust_summary']}")
    print()
    print("-"*60)
    print("⭐ QUALITY SCORE (Product Quality)")
    print("-"*60)
    print(f"   Score: {report['quality_score']} / 100")
    print(f"   Grade: {report['quality_grade']}")
    print(f"   Summary: {report['quality_summary']}")
    print()

    if report.get('red_flags_triggered'):
        print("-"*60)
        print("🚩 RED FLAGS TRIGGERED")
        print("-"*60)
        for i, flag in enumerate(report['red_flags_triggered'], 1):
            print(f"   {i}. {flag}")
        print()

    print("="*60)
    print()


def main():
    """
    Command-line interface for Project Veritas.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Project Veritas - Find truth in online reviews",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a product
  python main.py https://amazon.com/dp/B08N5WRWNW

  # Save report to file
  python main.py https://amazon.com/dp/B08N5WRWNW --output report.json

  # Quiet mode (no progress output)
  python main.py https://amazon.com/dp/B08N5WRWNW --quiet
        """
    )

    parser.add_argument(
        'url',
        type=str,
        help='Amazon product URL to analyze'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path for JSON report (optional)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress output (only show final report)'
    )

    args = parser.parse_args()

    # Run analysis
    report = run_veritas(args.url, output_file=args.output, verbose=not args.quiet)

    # Print JSON output if quiet mode (for piping)
    if args.quiet:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
