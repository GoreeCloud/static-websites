"""Original GC UI design-system specimens for the undeployed retained design route.

Uses only the exact pinned Foundations 1.0.1 CSS token names, not predecessor
markup/assets or invented platform-state assertions.
"""
from html import escape

SPECIMENS = (
    ("Canvas", "gc-role-canvas", "Application background and foreground",
     "--gc-v1-color-canvas", "--gc-v1-color-on-canvas"),
    ("Raised surface", "gc-role-surface", "Readable, elevated content",
     "--gc-v1-color-surface-raised", "--gc-v1-color-on-surface"),
    ("Primary", "gc-role-primary", "High-priority actions and emphasis",
     "--gc-v1-color-primary", "--gc-v1-color-on-primary"),
    ("Tonal surface", "gc-role-tonal", "Supporting information and separation",
     "--gc-v1-color-surface-tonal", "--gc-v1-color-on-surface"),
)


def render_design_specimens(foundations_css: str) -> str:
    for _, _, _, background, foreground in SPECIMENS:
        if background not in foundations_css or foreground not in foundations_css:
            raise ValueError("Missing pinned GC UI semantic role")
    samples = "".join(
        '<article class="gc-specimen-item ' + escape(css_class, quote=True) +
        '"><div class="gc-specimen-color"><span class="gc-specimen-color-label">' +
        escape(label) + '</span></div><div class="gc-specimen-description">' +
        '<h3>' + escape(label) + '</h3><p>' + escape(description) +
        '</p><code>' + escape(bg) + '</code></div></article>'
        for label, css_class, description, bg, _ in SPECIMENS
    )
    return (
        '<section class="section gc-specimens" id="specimens" '
        'aria-labelledby="specimens-title">'
        '<p class="eyebrow">Scoped GC UI Foundations 1.0.1</p>'
        '<h2 id="specimens-title">Adaptive colors in context</h2>'
        '<p class="section-lead">Switch System, Light, or Dark in the header. '
        'These four swatches read the actual pinned semantic tokens and adapt '
        'without replacing the GoreeCloud brand or making operational claims.</p>'
        '<div class="gc-specimen-grid">' + samples + '</div>'
        '<div class="gc-specimen-interaction">'
        '<h3>Interaction and focus</h3>'
        '<p>Use Tab to inspect keyboard focus. Controls follow the same '
        'theme and target rules used throughout this isolated preview.</p>'
        '<div class="gc-specimen-actions">'
        '<a class="primary-action" href="/platform-systems/#gc-ui">'
        'GC UI platform authority</a>'
        '<a class="gc-specimen-secondary" href="/contact/">Contact GoreeCloud</a>'
        '</div></div>'
        '<p class="section-lead">This is a scoped token specimen—not full '
        'component-system certification, contrast auditing, or website '
        'migration acceptance.</p></section>'
    )
