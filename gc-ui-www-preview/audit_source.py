#!/usr/bin/env python3
"""Report conservative public-content gaps without declaring site parity."""
from html.parser import HTMLParser
from pathlib import Path
import json
from build_routes import OUT, REPOSITORY, _namespace

class Content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.tags = {"h1": 0, "h2": 0, "h3": 0, "article": 0,
                     "input": 0, "button": 0, "a": 0}
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.inside = True
        if not self.inside:
            return
        if tag in self.tags:
            self.tags[tag] += 1
        if tag == "a":
            link = dict(attrs).get("href", "")
            if link.startswith("/") and not link.startswith("//"):
                self.links.add(link)

    def handle_endtag(self, tag):
        if tag == "main":
            self.inside = False

def inspect(path):
    parser = Content()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser

def audit():
    rows = []
    for entry in _namespace():
        source = inspect(REPOSITORY / entry["source"])
        target = OUT / ("index.html" if entry["path"] == "/"
                        else entry["id"] + "/index.html")
        candidate = inspect(target)
        missing = sorted(source.links - candidate.links)
        gaps = {tag: max(0, count - candidate.tags[tag])
                for tag, count in source.tags.items()}
        rows.append({"route": entry["path"], "source": source.tags,
                     "candidate": candidate.tags, "missingMainContentLinks": missing,
                     "unrepresentedElements": gaps,
                     "sourceArticleCount": source.tags["article"],
                     "candidateArticleCount": candidate.tags["article"],
                     "featureParityVerified": False})
    return {"schema": "gc-ui-public-source-gap-audit.v1",
            "productionChanged": False, "contentParityVerified": False,
            "browserAccessibilityAccepted": False, "routes": rows}

if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, sort_keys=True, indent=2))
    if len(report["routes"]) != 11:
        raise SystemExit("retained website route inventory changed")
