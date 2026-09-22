from bs4 import BeautifulSoup
from typing import List, Union
from website_analytics.url_utils import resolve_url, is_http_url


def extract_links(html_content: Union[str, bytes], base_url: str) -> List[str]:
    """Parse HTML and extract resolved HTTP/HTTPS URLs from <a href="..."> elements."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    discovered_urls = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()
        if (
            not href
            or href.startswith("#")
            or href.startswith("javascript:")
            or href.startswith("mailto:")
            or href.startswith("tel:")
        ):
            continue

        resolved = resolve_url(base_url, href)
        if resolved and is_http_url(resolved):
            discovered_urls.append(resolved)

    return discovered_urls
