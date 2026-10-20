"""Audit links and control references of the separate GC UI candidate."""
from html.parser import HTMLParser
from pathlib import Path
import json
from build_routes import OUT, PATHS
from public_links import acceptable

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.uses=[]
        self.hrefs=[]
        self.labels=set()
        self.inputs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids: raise ValueError("duplicate ID")
            self.ids.add(a["id"])
        for key in ("aria-controls","aria-labelledby","aria-describedby"):
            self.uses.extend(a.get(key,"").split())
        if tag=="a": self.hrefs.append(a.get("href",""))
        if tag=="label" and a.get("for"):self.labels.add(a["for"])
        if tag=="input": self.inputs.append((a.get("id"),a.get("aria-label")))
def audit():
    checked=[]
    pages={}
    for ident,path in PATHS.items():
        target=OUT/("index.html" if path=="/" else ident+"/index.html")
        p=Page();p.feed(target.read_text(encoding="utf-8"))
        pages[path]=p
        if set(p.uses)-p.ids:raise ValueError("broken ARIA reference: "+path)
        if any(not name and identity not in p.labels for identity,name in p.inputs):
            raise ValueError("unlabeled field: "+path)
        for href in p.hrefs:
            if href.startswith("mailto:") and not acceptable(href):
                raise ValueError("unapproved public mail recipient: "+path)
            if href.startswith("#") and href[1:] not in p.ids:raise ValueError("broken anchor: "+path)
            if href.startswith("/") and not href.startswith("//"):
                base=href.split("#",1)[0].split("?",1)[0]
                if base not in PATHS.values():raise ValueError("unknown route: "+base)
        checked.append(path)
    for src,page in pages.items():
        for link in page.hrefs:
            if link.startswith("/") and not link.startswith("//") and "#" in link:
                dest,frag=link.split("#",1)
                if not frag or frag not in pages[dest].ids:
                    raise ValueError("missing cross-route target: "+src+" "+link)
    return {"checkedRoutes":checked,"deployed":False,"accepted":False}
if __name__=="__main__":print(json.dumps(audit(),sort_keys=True))
