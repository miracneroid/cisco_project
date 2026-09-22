from typing import List
from website_analytics.models import LinkResult, AnalyticsSummary, ReportData


def analyze_results(results: List[LinkResult]) -> ReportData:
    """Analyze a list of LinkResults and return a complete ReportData object."""
    if not results:
        return ReportData(summary=AnalyticsSummary(), links=[])

    total_links = len(results)
    internal_links = sum(1 for r in results if r.link_type == "Internal")
    external_links = sum(1 for r in results if r.link_type == "External")
    broken_links = sum(1 for r in results if r.is_broken)

    max_latency_ms = max((r.latency_ms for r in results), default=0.0)
    max_bytes = max((r.bytes_transferred for r in results), default=0)

    summary = AnalyticsSummary(
        total_links=total_links,
        internal_links=internal_links,
        external_links=external_links,
        broken_links=broken_links,
        max_latency_ms=max_latency_ms,
        max_bytes_transferred=max_bytes,
    )

    return ReportData(summary=summary, links=results)
