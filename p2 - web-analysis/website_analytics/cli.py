import argparse
import sys
from typing import List, Optional

from website_analytics.crawler import WebCrawler
from website_analytics.analyzer import analyze_results
from website_analytics.reporter import render_terminal_report
from website_analytics.exporters import export_json, export_csv


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="analyze_links",
        description="Crawl and analyze website links to generate detailed analytics reports.",
    )
    parser.add_argument("url", help="Target website URL to analyze (e.g. https://www.python.org/)")
    parser.add_argument(
        "--to",
        choices=["terminal", "json", "csv"],
        default="terminal",
        help="Report output format (terminal, json, or csv). Default: terminal",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum crawl depth for internal links (default: 2)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Number of concurrent worker threads (default: 10)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP request timeout in seconds (default: 10.0)",
    )
    return parser


def main(cli_args: Optional[List[str]] = None) -> int:
    """CLI execution entrypoint."""
    parser = build_parser()
    args = parser.parse_args(cli_args)

    target_url = args.url
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    crawler = WebCrawler(
        start_url=target_url,
        max_depth=args.max_depth,
        workers=args.workers,
        timeout=args.timeout,
    )

    try:
        results = crawler.crawl()
    finally:
        crawler.fetcher.close()

    report_data = analyze_results(results)

    if args.to == "json":
        export_json(report_data, output=sys.stdout)
    elif args.to == "csv":
        export_csv(report_data, output=sys.stdout)
    else:
        render_terminal_report(report_data, output=sys.stdout)

    return 0
