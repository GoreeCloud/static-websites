"""Extract verified publication metadata for an isolated GC UI candidate.

SEO metadata from the retained public website is a *migration comparison input*,
not permission to index or publish the generated preview.
"""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ORIGIN = "https://www.goreecloud.com"
SOCIAL_IMAGE = ORIGIN + "/assets/social-preview.png"

class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.within_head = False
        self.in_title = False
        self.title_parts = []
        self.meta = {}
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "head":
            self.within_head = True
        if not self.within_head:
            return
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = attr.get("property") or attr.get("name")
            if key:
                if key in self.meta:
                    raise ValueError("duplicate source metadata field: " + key)
                self.meta[key] = attr.get("content", "")
        elif tag == "link" and attr.get("rel") == "canonical":
            self.canonicals.append(attr.get("href", ""))

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.within_head = False

def extract_public_metadata(source: Path, route: str, design_title: str,
                            design_description: str) -> dict:
    if source.is_symlink() or not source.is_file():
        raise ValueError("unsafe source metadata file")
    parser = Head()
    parser.feed(source.read_text(encoding="utf-8"))
    canonical = ORIGIN + route
    if parser.canonicals != [canonical]:
        raise ValueError("unexpected source canonical for " + route)
    meta = parser.meta
    required = ("description", "og:type", "og:site_name", "og:title",
                "og:description", "og:url", "og:image", "twitter:card")
    if any(not meta.get(name) for name in required):
        raise ValueError("incomplete published metadata for " + route)
    if (meta["og:type"] != "website" or meta["og:site_name"] != "GoreeCloud"
            or meta["og:url"] != canonical or meta["og:image"] != SOCIAL_IMAGE
            or meta["twitter:card"] != "summary_large_image"):
        raise ValueError("unapproved published metadata for " + route)
    title = "".join(parser.title_parts).strip()
    description = meta["description"].strip()
    og_title = meta["og:title"].strip()
    og_description = meta["og:description"].strip()
    if route == "/design/":
        # The published site has not yet removed a permanently retired
        # design authority. The candidate must NOT perpetuate this claim.
        title = design_title + " — GoreeCloud"
        description = design_description
        og_title, og_description = title, description
    elif (not title or "glaze" in title.lower() or
          "glaze" in description.lower() or "glaze" in og_title.lower()
          or "glaze" in og_description.lower()):
        raise ValueError("inconsistent or obsolete source metadata for " + route)
    if (not 10 <= len(title) <= 130 or not 30 <= len(description) <= 350
            or not 10 <= len(og_title) <= 130 or not 30 <= len(og_description) <= 350
            or "\x00" in title + description):
        raise ValueError("source metadata outside bounds")
    return {"title": title, "description": description,
            "og_title": og_title, "og_description": og_description,
            "canonical": canonical, "social_image": SOCIAL_IMAGE}


def render_preview_metadata(metadata: dict) -> str:
    # noindex MUST stay in the page renderer; publication is not authorized.
    title = escape(metadata["title"])
    description = escape(metadata["description"], quote=True)
    url = escape(metadata["canonical"], quote=True)
    social = escape(metadata["social_image"], quote=True)
    return (
        '  <title>' + title + '</title>\n'
        '  <meta name="description" content="' + description + '">\n'
        '  <link rel="canonical" href="' + url + '">\n'
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="GoreeCloud">\n'
        '  <meta property="og:title" content="' + escape(metadata["og_title"], quote=True) + '">\n'
        '  <meta property="og:description" content="' + description + '">\n'
        '  <meta property="og:url" content="' + url + '">\n'
        '  <meta property="og:image" content="' + social + '">\n'
        '  <meta name="twitter:card" content="summary_large_image">'
    )
