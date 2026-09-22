class AnalyticsError(Exception):
    """Base exception for Website Analytics application."""
    pass


class InvalidURLError(AnalyticsError):
    """Raised when an invalid or malformed URL is supplied."""
    pass


class FetchError(AnalyticsError):
    """Raised when an HTTP fetch fails catastrophically."""
    pass
