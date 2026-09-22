from website_analytics.models import LinkResult
from website_analytics.analyzer import analyze_results


def test_analyze_results():
    results = [
        LinkResult(
            url="https://example.com/",
            link_type="Internal",
            status_code=200,
            latency_ms=150.0,
            bytes_transferred=5000,
        ),
        LinkResult(
            url="https://example.com/about",
            link_type="Internal",
            status_code=200,
            latency_ms=250.0,
            bytes_transferred=8000,
        ),
        LinkResult(
            url="https://external.org/",
            link_type="External",
            status_code=200,
            latency_ms=400.0,
            bytes_transferred=2000,
        ),
        LinkResult(
            url="https://example.com/broken",
            link_type="Internal",
            status_code=404,
            latency_ms=50.0,
            bytes_transferred=100,
        ),
    ]

    report = analyze_results(results)
    s = report.summary

    assert s.total_links == 4
    assert s.internal_links == 3
    assert s.external_links == 1
    assert s.broken_links == 1
    assert s.max_latency_ms == 400.0
    assert s.max_bytes_transferred == 8000
