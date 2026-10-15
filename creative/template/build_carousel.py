#!/usr/bin/env python3
"""Render square carousel cards (1080x1080) from a spec: a real photo per card, a bold headline
in a box, a short sub line, and an optional badge. The last card can be a plain brand-colour CTA.

Usage: python3 creative/template/build_carousel.py spec.json
Spec (paths relative to the spec file unless absolute):
{
  "out_dir": "renders/carousel",
  "cards": [
    {"photo": "/abs/meter.jpg", "focus": [0.5, 0.5], "headline": "KAPILARNA VLAGA?", "sub": "Boja se ljušti uz pod?",
     "badge": "BESPLATNA PONUDA", "pos": "bottom"},
    {"cta": true, "headline": "Zatražite besplatnu ponudu", "sub": "Kratki obrazac · javljamo se brzo", "lines": ["✓ ...", "✓ ..."]}
  ]
}
"focus" picks the crop centre (0-1, 0-1) when the photo isn't square. "pos" is top or bottom.
"""
import json, pathlib, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = pathlib.Path(__file__).parent
BLUE, CYAN, INK, WHITE = (52, 131, 250), (34, 195, 255), (30, 30, 36), (250, 251, 255)
S = 1080


def font(w, size):
    return ImageFont.truetype(str(HERE / f"Manrope-{w}.ttf"), size)


def wrap(draw, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])


def square(photo, focus, zoom=1.0):
    im = ImageOps.exif_transpose(Image.open(photo)).convert("RGB")
    w, h = im.size; side = int(min(w, h) / zoom)
    fx, fy = focus
    x = int(min(max(fx * w - side / 2, 0), w - side)); y = int(min(max(fy * h - side / 2, 0), h - side))
    return im.crop((x, y, x + side, y + side)).resize((S, S), Image.LANCZOS)


def boxed(draw, lines, f, y, fill, color, pad=26, gap=10, align_bottom=False):
    hts = [draw.textbbox((0, 0), l, font=f)[3] for l in lines]
    total = sum(hts) + gap * (len(lines) - 1)
    if align_bottom: y -= total + 2 * pad
    for l, ht in zip(lines, hts):
        tw = draw.textlength(l, font=f)
        x = (S - tw) / 2
        draw.rounded_rectangle((x - pad, y, x + tw + pad, y + ht + 2 * pad - 6), 14, fill=fill)
        draw.text((x, y + pad - 8), l, font=f, fill=color)
        y += ht + 2 * pad - 6 + gap
    return y


def stack_h(draw, lines, f, pad, gap=10):
    return sum(draw.textbbox((0, 0), l, font=f)[3] + 2 * pad - 6 for l in lines) + gap * (len(lines) - 1)


def photo_card(c):
    im = square(c["photo"], c.get("focus", [0.5, 0.5]), c.get("zoom", 1.0))
    # darken the text side a little so white text always reads
    grad = Image.new("L", (1, S))
    bottom = c.get("pos", "bottom") == "bottom"
    for yy in range(S):
        t = yy / S if bottom else 1 - yy / S
        grad.putpixel((0, yy), int(150 * max(0, t - 0.45) / 0.55))
    im = Image.composite(Image.new("RGB", (S, S), (0, 0, 0)), im, grad.resize((S, S)))
    d = ImageDraw.Draw(im)
    hf, sf = font(800, c.get("size", 78)), font(600, 44)
    hl = wrap(d, c["headline"], hf, S - 160)
    sl = [x for part in c.get("sub", "").split("|") for x in wrap(d, part.strip(), sf, S - 140)] if c.get("sub") else []
    if bottom:
        sub_h = stack_h(d, sl, sf, 18) if sl else 0
        y = S - 60 - sub_h - (14 if sl else 0)
        y_top = y - stack_h(d, hl, hf, 26)
        boxed(d, hl, hf, y_top, BLUE, WHITE)
        if sl: boxed(d, sl, sf, y + 14, INK, WHITE, pad=18)
    else:
        y = boxed(d, hl, hf, 70, BLUE, WHITE)
        if sl: boxed(d, sl, sf, y + 4, INK, WHITE, pad=18)
    if c.get("badge"):
        bf = font(800, 38); tw = d.textlength(c["badge"], font=bf)
        d.rounded_rectangle((S - tw - 90, 40, S - 40, 112), 36, fill=CYAN)
        d.text((S - tw - 65, 52), c["badge"], font=bf, fill=INK)
    return im


def cta_card(c):
    im = Image.new("RGB", (S, S), BLUE); d = ImageDraw.Draw(im)
    hf, sf, lf = font(800, 92), font(600, 46), font(800, 50)
    y = 170
    for l in wrap(d, c["headline"], hf, S - 160):
        d.text(((S - d.textlength(l, font=hf)) / 2, y), l, font=hf, fill=WHITE); y += 112
    y += 30
    for l in c.get("lines", []):
        x = (S - d.textlength(l, font=lf) - 64) / 2
        d.line([(x, y + 34), (x + 16, y + 50), (x + 44, y + 16)], fill=CYAN, width=9, joint="curve")
        d.text((x + 64, y), l, font=lf, fill=WHITE); y += 78
    if c.get("sub"):
        bw = d.textlength(c["sub"], font=sf)
        d.rounded_rectangle(((S - bw) / 2 - 40, S - 230, (S + bw) / 2 + 40, S - 130), 50, fill=WHITE)
        d.text(((S - bw) / 2, S - 212), c["sub"], font=sf, fill=BLUE)
    return im


def run(spec_path):
    sp = pathlib.Path(spec_path).resolve(); spec = json.loads(sp.read_text())
    rel = lambda p: str(p if pathlib.Path(p).is_absolute() else (sp.parent / p).resolve())
    out = pathlib.Path(rel(spec["out_dir"])); out.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, c in enumerate(spec["cards"], 1):
        if "photo" in c: c["photo"] = rel(c["photo"])
        im = cta_card(c) if c.get("cta") else photo_card(c)
        p = out / f"card{i}.jpg"; im.save(p, quality=92); paths.append(p)
    strip = Image.new("RGB", (360 * len(paths), 360), WHITE)
    for i, p in enumerate(paths): strip.paste(Image.open(p).resize((360, 360)), (360 * i, 0))
    strip.save(out / "strip.jpg", quality=88)
    print(*paths, out / "strip.jpg")


if __name__ == "__main__":
    run(sys.argv[1])
