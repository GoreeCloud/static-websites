"""Extract text from reviewed public pages; never reuse old HTML or CSS."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import re

RETIRED = re.compile("glaze", re.I)
GC_UI_CARD = ("GoreeCloud UI (GC UI)",
    "Integral Platform System five of nine. Foundations 1.0.1 is a scoped stable release; "
    "broader original UI components and consumer migration are not yet accepted.")

class CardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.main = False
        self.card = False
        self.parts = []
        self.cards = []
        self.heading = ""
        self.heading_on = False
        self.excluded = False

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.main = True
        if self.main and tag == "article":
            if self.card:
                raise ValueError("nested public article")
            self.card, self.parts, self.heading = True, [], ""
        if self.card and tag == "h3":
            self.heading_on = True
        if self.card and tag in ("script", "style", "svg"):
            self.excluded = True

    def handle_data(self, data):
        if self.card and not self.excluded:
            value = " ".join(data.split())
            if value:
                self.parts.append(value)
                if self.heading_on:
                    self.heading += value + " "

    def handle_endtag(self, tag):
        if tag == "h3":
            self.heading_on = False
        if tag in ("script", "style", "svg"):
            self.excluded = False
        if tag == "article" and self.card:
            content = " ".join(self.parts)
            label = self.heading.strip() or (self.parts[0] if self.parts else "")
            if not label:
                raise ValueError("empty article")
            if not RETIRED.search(content):
                self.cards.append((label[:140], content[:2000]))
            self.card = False
        if tag == "main":
            self.main = False

def extract(path: Path, route: str):
    if not path.is_file() or path.is_symlink():
        raise ValueError("unverified retained source")
    parser = CardParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if parser.card or parser.main:
        raise ValueError("malformed public source")
    cards = parser.cards
    if route == "design":
        cards = [GC_UI_CARD,
                 ("Scoped foundation", "Semantic tokens, adaptive color and browser theme controls are included in Foundations 1.0.1."),
                 ("Open acceptance", "Full website adoption, assistive technology and production release are not yet accepted.")]
    elif route in ("platform-systems", "security", "privacy"):
        cards.append(GC_UI_CARD)
    return cards

def render(cards, route=""):
    anchors = {"Privacy Shield": "privacy-shield",
               "Wardveil Security": "wardveil-security",
               "GoreeCloud UI (GC UI)": "gc-ui"} if route == "platform-systems" else {}
    return ('<section class="section" id="source-content" aria-labelledby="source-content-title">'
       '<p class="eyebrow">Public-source text reconciliation</p>'
       '<h2 id="source-content-title">Existing product information</h2>'
       '<p class="section-lead">Extracted public text, with superseded design claims omitted. '
       'Not functional or content-parity acceptance.</p><div class="route-grid">' +
       "".join('<article class="panel candidate-content-card"' +
               (' id="' + anchors[title] + '"' if title in anchors else '') +
               '><h3>' + escape(title) +
               '</h3><p>' + escape(text) + '</p></article>' for title,text in cards) +
       '</div></section>')
