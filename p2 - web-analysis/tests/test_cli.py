import io
from unittest.mock import patch
from website_analytics.cli import build_parser, main
from website_analytics.models import LinkResult, ReportData, AnalyticsSummary


def test_build_parser():
    parser = build_parser()
    args = parser.parse_args(["https://example.com", "--to=json", "--max-depth=3"])
    assert args.url == "https://example.com"
    assert args.to == "json"
    assert args.max_depth == 3


@patch("website_analytics.cli.WebCrawler")
def test_cli_main_json_output(mock_crawler_cls):
    mock_instance = mock_crawler_cls.return_value
    mock_instance.crawl.return_value = [
        LinkResult(
            url="https://example.com",
            link_type="Internal",
            status_code=200,
            latency_ms=100.0,
            bytes_transferred=500,
            content_type="text/html",
        )
    ]

    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        exit_code = main(["https://example.com", "--to=json"])
        assert exit_code == 0
        output_str = fake_out.getvalue()
        assert '"total_links": 1' in output_str
