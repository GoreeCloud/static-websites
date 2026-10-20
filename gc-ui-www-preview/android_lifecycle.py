"""Recreate public Android lifecycle groups with original GC UI markup.

Read only reviewed retained source; never copy old CSS, icons or scripting.
"""
from html import escape
from pathlib import Path
import re

from source_cards import CardParser

LIFECYCLES = (
    ("planned", "Planned"),
    ("active-development", "Active development"),
    ("release-candidate", "Release Candidate"),
    ("stable", "Stable"),
)
SECTION = re.compile(
    r'<section\b[^>]*\bdata-android-lifecycle="([^"]+)"[^>]*>(.*?)</section>',
    re.S | re.I,
)


def extract_lifecycles(path: Path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("unsafe Android source")
    data = path.read_text(encoding="utf-8")
    sections = SECTION.findall(data)
    if [name for name, _ in sections] != [name for name, _ in LIFECYCLES]:
        raise ValueError("missing or reordered reviewed Android lifecycle groups")
    result = []
    for (name, title), (found, markup) in zip(LIFECYCLES, sections):
        if found != name or '<section' in markup.lower():
            raise ValueError("nested or mismatched Android lifecycle")
        parser = CardParser()
        parser.feed("<main>" + markup + "</main>")
        if parser.main or parser.card or not parser.cards:
            raise ValueError("empty or malformed Android lifecycle " + name)
        result.append((name, title, parser.cards))
    if len(result[0][2]) != 4 or len(result[1][2]) != 16:
        raise ValueError("Android planned/development inventory changed; review required")
    return result


def render_android(source: Path):
    sections = extract_lifecycles(source)
    links = "".join(
        '<a href="#' + escape(name, quote=True) + '">' + escape(title) + "</a>"
        for name, title, _ in sections
    )
    groups = []
    for name, title, cards in sections:
        card_html = "".join(
            '<article class="panel candidate-content-card">'
            '<h3>' + escape(label) + '</h3><p>' + escape(text) + '</p></article>'
            for label, text in cards
        )
        groups.append(
            '<section class="android-lifecycle" id="' + escape(name, quote=True) +
            '" aria-labelledby="' + escape(name, quote=True) + '-title">'
            '<div class="lifecycle-heading"><h3 id="' + escape(name, quote=True) +
            '-title">' + escape(title) + '</h3>'
            '<span class="lifecycle-count">' + str(len(cards)) +
            ' public-source entries</span></div>'
            '<div class="route-grid">' + card_html + '</div></section>'
        )
    return (
        '<section class="section" id="source-content" aria-labelledby="source-content-title">'
        '<p class="eyebrow">Android lifecycle / reviewed public source</p>'
        '<h2 id="source-content-title">Android products by lifecycle</h2>'
        '<p class="section-lead">Source-backed categories, not release certification. '
        'Only each component’s current evidence establishes its release status.</p>'
        '<nav class="lifecycle-nav" aria-label="Android lifecycle sections">' + links +
        '</nav>' + "".join(groups) + '</section>'
    )
