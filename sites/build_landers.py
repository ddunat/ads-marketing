#!/usr/bin/env python3
"""Build ad landing pages from specs.

Each ad gets one spec in sites/landers/<market>-<slug>.json (see landers/README.md).
This renders sites/public/<market>/<slug>.html from templates/lander.html and writes
sites/landers/index.json, which server.js reads to route pages and tag leads.

Run: python3 sites/build_landers.py   (fails loudly on missing fields or TODO values)
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
MARKETS = json.loads((ROOT / "landers/markets.json").read_text())
TEMPLATE = (ROOT / "templates/lander.html").read_text()
REQUIRED = ["market", "path", "key", "ad", "service", "hot", "title", "meta_description",
            "eyebrow", "h1", "sub", "steps", "how", "faq", "bottom_cta", "sticky_text", "sticky_cta"]
e = lambda s: html.escape(str(s), quote=False).replace('"', "&quot;")


def todo_check(obj, where):
    if isinstance(obj, str) and "TODO" in obj:
        sys.exit(f"{where}: still has a TODO value: {obj[:80]}")
    if isinstance(obj, dict):
        for k, v in obj.items(): todo_check(v, f"{where}.{k}")
    if isinstance(obj, list):
        for i, v in enumerate(obj): todo_check(v, f"{where}[{i}]")


def section_vsl(v):
    if not v: return ""
    return (f'  <section class="vsl">\n    <h2>{e(v["title"])}</h2>\n'
            f'    <video controls playsinline preload="none" poster="{e(v["poster"])}" width="720" height="1280" aria-label="{e(v["label"])}">'
            f'<source src="{e(v["src"])}" type="video/mp4"></video>\n    <p class="small">{e(v.get("note", "Captions on. Tap to play."))}</p>\n  </section>\n')


def section_how(h):
    rows = []
    for item in h["items"]:
        if "figure" in item:
            f = item["figure"]
            imgs = "".join(f'<img src="{e(i["src"])}" width="{i["w"]}" height="{i["h"]}" loading="lazy" decoding="async" alt="{e(i["alt"])}"' + (f' style="max-width:{i["max_w"]}px"' if i.get("max_w") else "") + ">" for i in f["images"])
            cls = ' class="pair"' if len(f["images"]) == 2 else ""
            inner = f"<div>{imgs}</div>" if len(f["images"]) == 2 else imgs
            rows.append(f'      <figure{cls}>{inner}<figcaption>{e(f["caption"])}</figcaption></figure>')
        else:
            rows.append(f'      <div><b class="n">{item["n"]}</b><span><b>{e(item["title"])}</b> {e(item["text"])}</span></div>')
    return f'  <section>\n    <h2>{e(h["title"])}</h2>\n    <div class="steps">\n' + "\n".join(rows) + "\n    </div>\n  </section>\n"


def section_price(p):
    if not p: return ""
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in p["rows"])
    anchor = f'    <p class="anchor">{e(p["anchor"])}</p>\n' if p.get("anchor") else ""
    return (f'  <section>\n    <h2>{e(p["title"])}</h2>\n{anchor}    <table>\n      {rows}\n    </table>\n'
            f'    <p class="small">{e(p.get("note", ""))}</p>\n  </section>\n')


def section_faq(items, title):
    qa = "\n".join(f"    <details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    return f"  <section>\n    <h2>{e(title)}</h2>\n{qa}\n  </section>\n"


def build(spec_path):
    spec = json.loads(spec_path.read_text())
    missing = [k for k in REQUIRED if k not in spec]
    if missing: sys.exit(f"{spec_path.name}: missing {missing}")
    m = MARKETS[spec["market"]]
    todo_check(m, spec["market"]); todo_check(spec, spec_path.name)
    if not re.fullmatch(r"/[a-z0-9-]+", spec["path"]): sys.exit(f"{spec_path.name}: bad path {spec['path']}")
    steps = spec["steps"] + [m["contact_step"]]
    market_js = dict(m["ui"], phone_re=m["phone_re"])
    fill = {
        "lang": m["lang"], "title": e(spec["title"]), "meta_description": e(spec["meta_description"]),
        "eyebrow": e(spec["eyebrow"]), "h1": e(spec["h1"]), "sub": e(spec["sub"]),
        "director_label": e(spec.get("director_label", m["director_label"])),
        "cred_lines": "".join(spec.get("cred_lines", m["cred_lines"])),
        "proof_card": spec.get("proof_card", m["proof_card"]),
        "vsl": section_vsl(spec.get("vsl")), "how": section_how(spec["how"]),
        "price": section_price(spec.get("price")),
        "faq": section_faq(spec["faq"], spec.get("faq_title", "Questions" if spec["market"] == "au" else "Pitanja")),
        "bottom_cta": e(spec["bottom_cta"]), "footer": e(spec.get("footer", m["footer"])),
        "sticky_text": e(spec["sticky_text"]), "sticky_cta": e(spec["sticky_cta"]),
        "steps_json": json.dumps(steps, ensure_ascii=False), "market_js": json.dumps(market_js, ensure_ascii=False),
    }
    out = TEMPLATE
    for k, v in fill.items(): out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{\w+\}\}", out)
    if left: sys.exit(f"{spec_path.name}: unfilled {left}")
    dest = ROOT / "public" / spec["market"] / (spec["path"].strip("/") + ".html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)
    return {"market": spec["market"], "path": spec["path"], "file": f'{spec["market"]}/{dest.name}',
            "key": spec["key"], "ad": spec["ad"], "service": spec["service"], "hot": spec["hot"]}


if __name__ == "__main__":
    specs = sorted(p for p in (ROOT / "landers").glob("*.json") if p.name not in ("markets.json", "index.json"))
    index = [build(p) for p in specs]
    seen = set()
    for x in index:
        k = (x["market"], x["path"])
        if k in seen: sys.exit(f"duplicate page {k}")
        seen.add(k)
    (ROOT / "landers/index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")
    print(f"built {len(index)} page(s):", ", ".join(f'{x["market"]}{x["path"]}' for x in index))
