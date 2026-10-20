"""Safe outbound navigation extracted as links, without legacy markup."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ALLOWED_HOSTS = {
    "github.com", "instagram.com", "www.instagram.com",
    "www.threads.com", "www.tiktok.com", "x.com",
    "www.reddit.com", "www.pinterest.com",
}
ALLOWED_PATHS = {
    "/", "/platform-systems/", "/suite/", "/android/", "/office-suite/",
    "/firefox/", "/github/", "/contact/", "/design/", "/security/", "/privacy/",
}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_main = False
        self.href = None
        self.label = []
        self.found = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.inside_main = True
        if tag == "a" and self.inside_main:
            self.href = dict(attrs).get("href")
            self.label = []

    def handle_data(self, text):
        if self.href is not None:
            self.label.append(text.strip())

    def handle_endtag(self, tag):
        if tag == "a" and self.href is not None:
            label = " ".join(x for x in self.label if x)
            if label and "glaze" not in label.lower() and acceptable(self.href):
                value = (self.href, label[:140])
                if value not in self.found:
                    self.found.append(value)
            self.href = None
        if tag == "main":
            self.inside_main = False

def acceptable(href):
    if not href or any(x in href for x in ("\\", "\r", "\n", "\t", " ")):
        return False
    if href in ALLOWED_PATHS:
        return True
    url = urlsplit(href)
    if url.scheme == "https":
        return bool(url.hostname in ALLOWED_HOSTS and not url.username and not url.password)
    if url.scheme == "mailto":
        return bool(url.path and "@" in url.path and not url.query and not url.fragment)
    return False

def render_links(source: Path):
    if source.is_symlink() or not source.is_file():
        raise ValueError("untrusted link source")
    parser = Links()
    parser.feed(source.read_text(encoding="utf-8"))
    if not parser.found:
        return ""
    contents = "".join(
        '<li><a href="' + escape(href, quote=True) + '" rel="noopener noreferrer">' +
        escape(label) + '</a></li>' for href, label in parser.found)
    return ('<section class="section" id="source-links" aria-labelledby="source-links-title">'
            '<h2 id="source-links-title">Published navigation and contact links</h2>'
            '<p class="section-lead">Links are carried over from the reviewed public-source'
            ' pages and limited to approved destinations.</p>'
            '<nav aria-label="Published source links"><ul class="public-link-list">' +
            contents + '</ul></nav></section>')
