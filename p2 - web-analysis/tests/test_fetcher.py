import httpx
from website_analytics.fetcher import Fetcher


def test_fetcher_success():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            headers={"content-type": "text/html; charset=utf-8"},
            content=b"<html>Hello</html>",
        )

    mock_client = httpx.Client(transport=httpx.MockTransport(mock_handler))
    fetcher = Fetcher(client=mock_client)

    result, content = fetcher.fetch("https://example.com/test", link_type="Internal")

    assert result.status_code == 200
    assert result.content_type == "text/html"
    assert result.bytes_transferred == len(b"<html>Hello</html>")
    assert result.latency_ms >= 0.0
    assert result.error is None
    assert content == b"<html>Hello</html>"


def test_fetcher_error():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused")

    mock_client = httpx.Client(transport=httpx.MockTransport(mock_handler))
    fetcher = Fetcher(client=mock_client)

    result, content = fetcher.fetch("https://broken.com", link_type="External")

    assert result.status_code is None
    assert result.is_broken is True
    assert result.error is not None
    assert content is None
