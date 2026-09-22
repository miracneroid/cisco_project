import io
import json
import csv
from website_analytics.models import LinkResult
from website_analytics.analyzer import analyze_results
from website_analytics.exporters import export_json, export_csv
from website_analytics.reporter import render_terminal_report


def test_export_json():
    results = [
        LinkResult(
            url="https://example.com/about",
            link_type="Internal",
            status_code=200,
            latency_ms=120.5,
            bytes_transferred=4500,
            content_type="text/html",
        )
    ]
    report = analyze_results(results)
    out = io.StringIO()
    export_json(report, output=out)

    data = json.loads(out.getvalue())
    assert "summary" in data
    assert "links" in data
    assert data["summary"]["total_links"] == 1
    assert data["links"][0]["url"] == "https://example.com/about"


def test_export_csv():
    results = [
        LinkResult(
            url="https://example.com/about",
            link_type="Internal",
            status_code=200,
            latency_ms=120.5,
            bytes_transferred=4500,
            content_type="text/html",
        )
    ]
    report = analyze_results(results)
    out = io.StringIO()
    export_csv(report, output=out)

    lines = out.getvalue().strip().splitlines()
    assert len(lines) == 2  # Header + 1 row
    assert "url,type,status_code" in lines[0]
    assert "https://example.com/about" in lines[1]


def test_render_terminal_report():
    results = [
        LinkResult(
            url="https://example.com/about",
            link_type="Internal",
            status_code=200,
            latency_ms=120.5,
            bytes_transferred=4500,
            content_type="text/html",
        )
    ]
    report = analyze_results(results)
    out = io.StringIO()
    render_terminal_report(report, output=out)

    text = out.getvalue()
    assert "Summary report:" in text
    assert "Total Links: 1" in text
    assert "/about" in text
