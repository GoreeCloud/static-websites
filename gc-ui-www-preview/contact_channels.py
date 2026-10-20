"""Build first-party GC UI contact and community cards from reviewed public links."""
from html import escape
from pathlib import Path

from public_links import Links, acceptable

CHANNELS = (
    ("Support", "mailto:support@goreecloud.com",
     "General questions, support requests, and product assistance."),
    ("Security reports", "mailto:security@goreecloud.com",
     "Report a security concern without sending credentials or secrets."),
    ("Public source", "/github/",
     "Explore public development and project repositories."),
)
SOCIAL = (
    ("Instagram", "https://instagram.com/goreecloud", "Visual updates"),
    ("Threads", "https://www.threads.com/@goreecloud", "Community discussions"),
    ("TikTok", "https://www.tiktok.com/@goreecloud", "Product demonstrations"),
    ("X", "https://x.com/GoreeCloud", "Technical announcements"),
    ("Reddit", "https://www.reddit.com/user/goreecloud/", "Detailed discussions"),
    ("Pinterest", "https://www.pinterest.com/goreecloud/", "Visual inspiration"),
)


def verified(source: Path):
    if source.is_symlink() or not source.is_file():
        raise ValueError("unsafe public contact source")
    parser = Links()
    parser.feed(source.read_text(encoding="utf-8"))
    present = {href for href, _ in parser.found}
    expected = {href for _, href, _ in CHANNELS + SOCIAL}
    if not expected <= present:
        raise ValueError("public contact channel inventory changed")
    if any(not acceptable(href) for href in expected):
        raise ValueError("unapproved public contact destination")
    return CHANNELS, SOCIAL


def render_contact(source: Path):
    channels, social = verified(source)

    def cards(entries):
        return "".join(
            '<article class="panel contact-channel">'
            '<h3>' + escape(name) + '</h3>'
            '<p>' + escape(description) + '</p>'
            '<a class="contact-channel-link" href="' + escape(href, quote=True) +
            '"' + (' rel="noopener noreferrer"' if href.startswith("https://") else '') +
            ' aria-label="Open ' + escape(name, quote=True) + '">'
            + ('Open channel' if href.startswith("https://") else
               'Open public source' if href.startswith("/") else 'Compose email') +
            '</a></article>'
            for name, href, description in entries
        )

    return (
        '<section class="section" id="contact-channels" aria-labelledby="contact-channels-title">'
        '<p class="eyebrow">Verified public routes</p>'
        '<h2 id="contact-channels-title">Choose the right contact channel</h2>'
        '<p class="section-lead">Use public support for general requests and the dedicated '
        'security address for disclosures. No private owner information is published.</p>'
        '<div class="route-grid">' + cards(channels) + '</div></section>'
        '<section class="section" id="social" aria-labelledby="social-title">'
        '<p class="eyebrow">Community</p><h2 id="social-title">GoreeCloud on social platforms</h2>'
        '<p class="section-lead">Six verified public accounts carried over from the '
        'current published source. External links open their respective providers.</p>'
        '<div class="route-grid">' + cards(social) + '</div></section>'
    )
