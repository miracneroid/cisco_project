from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class LinkResult:
    """Represents the analyzed metrics for a single crawled link."""

    url: str
    link_type: str  # "Internal" or "External"
    status_code: Optional[int] = None
    latency_ms: float = 0.0
    bytes_transferred: int = 0
    content_type: str = "Unknown"
    error: Optional[str] = None

    @property
    def is_broken(self) -> bool:
        """Determines if the link is considered broken (status >= 400 or network error)."""
        if self.error is not None:
            return True
        if self.status_code is None or self.status_code >= 400:
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary representation."""
        return {
            "url": self.url,
            "type": self.link_type,
            "status_code": self.status_code,
            "latency_ms": round(self.latency_ms, 2),
            "bytes_transferred": self.bytes_transferred,
            "content_type": self.content_type,
            "error": self.error,
        }


@dataclass
class AnalyticsSummary:
    """Represents aggregated summary statistics for the web analysis crawl."""

    total_links: int = 0
    internal_links: int = 0
    external_links: int = 0
    broken_links: int = 0
    max_latency_ms: float = 0.0
    max_bytes_transferred: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary representation."""
        return {
            "total_links": self.total_links,
            "internal_links": self.internal_links,
            "external_links": self.external_links,
            "broken_links": self.broken_links,
            "max_latency_ms": round(self.max_latency_ms, 2),
            "max_bytes_transferred": self.max_bytes_transferred,
        }


@dataclass
class ReportData:
    """Container holding summary statistics and all detailed link results."""

    summary: AnalyticsSummary
    links: List[LinkResult] = field(default_factory=list)
