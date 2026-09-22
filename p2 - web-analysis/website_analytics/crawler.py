import sys
import threading
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Set, Optional, Callable

from website_analytics.models import LinkResult
from website_analytics.fetcher import Fetcher
from website_analytics.parser import extract_links
from website_analytics.url_utils import normalize_url, is_internal_link, is_http_url


class WebCrawler:
    """Multithreaded bounded web crawler for site analysis."""

    def __init__(
        self,
        start_url: str,
        max_depth: int = 2,
        workers: int = 10,
        timeout: float = 10.0,
        fetcher: Optional[Fetcher] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
    ):
        self.start_url = normalize_url(start_url)
        self.max_depth = max_depth
        self.workers = workers
        self.timeout = timeout
        self.fetcher = fetcher or Fetcher(timeout=timeout)
        self.progress_callback = progress_callback or self._default_progress

        self._lock = threading.Lock()
        self.visited_urls: Set[str] = set()
        self.results: List[LinkResult] = []

    def _default_progress(self, msg: str) -> None:
        """Default progress updater that overwrites the terminal line."""
        sys.stdout.write(f"\r\033[K{msg}")
        sys.stdout.flush()

    def crawl(self) -> List[LinkResult]:
        """Execute the crawl using a thread pool and return all discovered LinkResults."""
        if not is_http_url(self.start_url):
            raise ValueError(f"Invalid starting HTTP/HTTPS URL: '{self.start_url}'")

        # Current level queue of (url, depth, link_type)
        current_level = [(self.start_url, 0, "Internal")]
        self.visited_urls.add(self.start_url)

        for depth in range(self.max_depth + 1):
            if not current_level:
                break

            next_level = []

            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                future_to_item = {
                    executor.submit(self._fetch_and_parse, url, d, l_type): (url, d, l_type)
                    for url, d, l_type in current_level
                }

                for future in as_completed(future_to_item):
                    item_url, item_depth, item_type = future_to_item[future]
                    try:
                        result, discovered = future.result()
                        with self._lock:
                            self.results.append(result)

                        # If internal and within depth limit, queue discovered links
                        if item_type == "Internal" and item_depth < self.max_depth and discovered:
                            for disc_url in discovered:
                                with self._lock:
                                    if disc_url not in self.visited_urls:
                                        self.visited_urls.add(disc_url)
                                        disc_type = (
                                            "Internal"
                                            if is_internal_link(self.start_url, disc_url)
                                            else "External"
                                        )
                                        next_level.append((disc_url, item_depth + 1, disc_type))
                    except Exception as e:
                        # Log unexpected thread failures gracefully
                        pass

            current_level = next_level

        # Clear progress line when finished
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

        return self.results

    def _fetch_and_parse(
        self, url: str, depth: int, link_type: str
    ) -> tuple[LinkResult, List[str]]:
        """Fetch a single URL, emit progress, and extract links if HTML and internal."""
        parsed_path = urlparse(url).path or "/"
        self.progress_callback(f"Fetching {parsed_path} ...")

        result, content_bytes = self.fetcher.fetch(url, link_type=link_type)

        discovered: List[str] = []
        if (
            link_type == "Internal"
            and result.status_code == 200
            and content_bytes
            and "text/html" in result.content_type.lower()
        ):
            discovered = extract_links(content_bytes, base_url=url)

        return result, discovered
