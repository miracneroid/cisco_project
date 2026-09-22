import time
import httpx
from typing import Tuple, Optional
from website_analytics.models import LinkResult


class Fetcher:
    """Handles HTTP network requests using httpx with precise latency measurement."""

    def __init__(
        self,
        timeout: float = 10.0,
        user_agent: str = "PyWebAnalytics/1.0",
        client: Optional[httpx.Client] = None,
    ):
        self.timeout = timeout
        self.user_agent = user_agent
        self.client = client or httpx.Client(
            follow_redirects=True,
            timeout=httpx.Timeout(timeout),
            headers={"User-Agent": self.user_agent},
        )

    def fetch(self, url: str, link_type: str = "Internal") -> Tuple[LinkResult, Optional[bytes]]:
        """Fetch a URL, record latency/bytes/headers, and return a LinkResult with body bytes."""
        start_time = time.perf_counter()
        try:
            response = self.client.get(url)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            content_type_header = response.headers.get("content-type", "Unknown")
            content_type = content_type_header.split(";")[0].strip() if content_type_header else "Unknown"

            content_bytes = response.content
            bytes_transferred = len(content_bytes)

            result = LinkResult(
                url=url,
                link_type=link_type,
                status_code=response.status_code,
                latency_ms=elapsed_ms,
                bytes_transferred=bytes_transferred,
                content_type=content_type,
                error=None,
            )
            return result, content_bytes

        except httpx.TimeoutException:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            result = LinkResult(
                url=url,
                link_type=link_type,
                status_code=None,
                latency_ms=elapsed_ms,
                bytes_transferred=0,
                content_type="Unknown",
                error="Timeout",
            )
            return result, None

        except httpx.HTTPError as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            result = LinkResult(
                url=url,
                link_type=link_type,
                status_code=None,
                latency_ms=elapsed_ms,
                bytes_transferred=0,
                content_type="Unknown",
                error=f"HTTPError: {type(e).__name__}",
            )
            return result, None

        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            result = LinkResult(
                url=url,
                link_type=link_type,
                status_code=None,
                latency_ms=elapsed_ms,
                bytes_transferred=0,
                content_type="Unknown",
                error=str(e),
            )
            return result, None

    def close(self) -> None:
        """Close the HTTP client connection pool."""
        self.client.close()
