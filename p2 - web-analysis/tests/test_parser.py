from website_analytics.parser import extract_links


def test_extract_links():
    html = """
    <html>
        <body>
            <a href="/about">About</a>
            <a href="https://external.org/page">External</a>
            <a href="mailto:test@example.com">Email</a>
            <a href="#section">Section</a>
        </body>
    </html>
    """
    base = "https://mysite.com/"
    links = extract_links(html, base)

    assert "https://mysite.com/about" in links
    assert "https://external.org/page" in links
    assert len(links) == 2  # mailto and #section excluded
