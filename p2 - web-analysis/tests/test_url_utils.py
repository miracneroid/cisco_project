import pytest
from website_analytics.url_utils import (
    normalize_url,
    resolve_url,
    is_http_url,
    get_domain,
    is_internal_link,
)


def test_normalize_url():
    assert normalize_url("HTTPS://EXAMPLE.COM/about#section") == "https://example.com/about"
    assert normalize_url("http://example.com:8080/path?query=1#frag") == "http://example.com:8080/path?query=1"


def test_resolve_url():
    base = "https://example.com/docs/index.html"
    assert resolve_url(base, "/about") == "https://example.com/about"
    assert resolve_url(base, "page2.html") == "https://example.com/docs/page2.html"
    assert resolve_url(base, "https://other.com") == "https://other.com"


def test_is_http_url():
    assert is_http_url("http://example.com") is True
    assert is_http_url("https://example.com/page") is True
    assert is_http_url("mailto:user@example.com") is False
    assert is_http_url("javascript:void(0)") is False


def test_get_domain():
    assert get_domain("https://www.example.com/about") == "example.com"
    assert get_domain("http://sub.example.com/") == "sub.example.com"


def test_is_internal_link():
    base = "https://example.com/"
    assert is_internal_link(base, "https://example.com/about") is True
    assert is_internal_link(base, "https://sub.example.com/page") is True
    assert is_internal_link(base, "https://google.com/") is False
