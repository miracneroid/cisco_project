import httpx
from website_analytics.fetcher import Fetcher
from website_analytics.crawler import WebCrawler


def test_crawler_depth_and_external_handling():
    site_pages = {
        "https://example.com": b'<html><a href="/about">About</a><a href="https://external.com">Ext</a></html>',
        "https://example.com/about": b"<html><a href=\"/contact\">Contact</a></html>",
        "https://example.com/contact": b"<html>Contact Page</html>",
        "https://external.com": b"<html>External Page</html>",
    }

    def mock_handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url in site_pages:
            return httpx.Response(
                status_code=200,
                headers={"content-type": "text/html"},
                content=site_pages[url],
            )
        return httpx.Response(status_code=404, content=b"Not Found")

    mock_client = httpx.Client(transport=httpx.MockTransport(mock_handler))
    fetcher = Fetcher(client=mock_client)

    crawler = WebCrawler(
        start_url="https://example.com",
        max_depth=1,
        workers=2,
        fetcher=fetcher,
        progress_callback=lambda msg: None,
    )

    results = crawler.crawl()
    urls_crawled = {r.url for r in results}

    assert "https://example.com" in urls_crawled
    assert "https://example.com/about" in urls_crawled
    assert "https://external.com" in urls_crawled
    # /contact should NOT be crawled because max_depth=1 (start=0, about=1)
    assert "https://example.com/contact" not in urls_crawled

    ext_result = next(r for r in results if r.url == "https://external.com")
    assert ext_result.link_type == "External"
