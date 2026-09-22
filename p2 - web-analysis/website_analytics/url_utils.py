from urllib.parse import urlparse, urljoin, urlunparse
from typing import Optional


def normalize_url(url: str) -> str:
    """Normalize a URL by stripping fragments, lowercasing scheme/hostname, and cleaning paths."""
    if not url:
        return ""
    parsed = urlparse(url.strip())
    # Lowercase scheme and netloc (hostname + port)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    
    # Remove fragment (#)
    fragment = ""
    
    # Reconstruct normalized URL
    normalized = urlunparse((scheme, netloc, parsed.path, parsed.params, parsed.query, fragment))
    return normalized


def resolve_url(base_url: str, href: str) -> str:
    """Resolve a relative or absolute href link against a base URL using urllib.parse.urljoin."""
    if not href:
        return ""
    href = href.strip()
    # Join relative or absolute path to base URL
    full_url = urljoin(base_url, href)
    return normalize_url(full_url)


def is_http_url(url: str) -> bool:
    """Check if the URL uses an HTTP or HTTPS scheme."""
    if not url:
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")


def get_domain(url: str) -> str:
    """Extract and normalize the domain/hostname from a URL."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    hostname = hostname.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


def is_internal_link(start_url: str, target_url: str) -> bool:
    """Determine whether target_url is internal relative to start_url by comparing domains."""
    start_domain = get_domain(start_url)
    target_domain = get_domain(target_url)

    if not start_domain or not target_domain:
        return False

    return start_domain == target_domain or target_domain.endswith("." + start_domain)
