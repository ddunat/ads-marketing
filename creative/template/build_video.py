#!/usr/bin/env python3
"""Build a finished 9:16 ad from a HeyGen talking-head render plus a spec.

This is the A2 v6 / VSL edit turned into a recipe (creative/template/TEXT-SPEC.md for the text rules):
hook boxes over the first ~2s, word-timed captions from HeyGen's SRT, B-roll and image overlays,
the report-ready notification, punch lines, then the live-form end card.

Usage: python3 creative/template/build_video.py spec.json
Spec (paths relative to the spec file unless absolute):
{
  "avatar": "renders/x-plain.mp4",          # HeyGen video_url download
  "srt": "renders/x.srt",                   # HeyGen caption_url download
  "hflip": true,                            # David's look is mirrored: flip so the shirt logo reads correctly
  "hook": {"box": "BIDDING AT AUCTION", "sub": "THIS WEEK?", "until": 2.0, "then": "Know this {before you bid.}"},
  "highlight": ["no cooling-off", "529"],   # words/phrases shown in cyan in captions ({...} in hook.then too)
  "replace": {"four point nine stars from five hundred and twenty-nine": "4.9 stars from 529"},
  "caption_top": [[17.0, 25.6]],            # windows where captions move to the top (an image overlay owns the bottom)
  "no_captions": [[35.2, 38.7]],            # windows with no captions (a punch owns the screen)
  "punches": [{"start": 35.2, "end": 38.7, "pos": "top", "text": "SAME-DAY REPORT\\N{OR YOUR MONEY BACK}"}],
  "overlays": [
    {"type": "broll", "clip": "library/house.mp4", "from": 3.0, "to": 5.8, "at": 4.2, "speed": 1.0, "zoom": true},
    {"type": "image", "src": "../template/assets/proofcard-au.png", "at": 17.1, "until": 25.5},
    {"type": "notif", "at": 35.2, "until": 38.7}
  ],
  "endcard": "../template/assets/endcard_rec.mp4",   # optional; appended after the talking head
  "out": "renders/x-final.mp4"
}
"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = HERE
CYAN, WHITE = "&H00FFC322&", "&H00FFFFFF&"
POP = r"{\fscx108\fscy108\t(0,100,\fscx100\fscy100)}"
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Manrope ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00241E1E,&H96000000,0,0,0,0,100,100,0,0,1,6,4,2,70,70,600,1
Style: CapTop,Manrope ExtraBold,88,&H00FFFFFF,&H00FFFFFF,&H00241E1E,&H96000000,0,0,0,0,100,100,0,0,1,6,4,8,70,70,330,1
Style: HookBox,Manrope ExtraBold,90,&H00FFFFFF,&H00FFFFFF,&H00FA8334,&H00FA8334,0,0,0,0,100,100,0,0,3,30,0,8,60,60,230,1
Style: HookSub,Manrope ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00241E1E,&H00241E1E,0,0,0,0,100,100,1,0,3,24,0,8,60,60,385,1
Style: PunchTop,Manrope ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00241E1E,&H00241E1E,0,0,0,0,100,100,1,0,3,34,0,8,50,50,560,1
Style: Punch,Manrope ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00241E1E,&H00241E1E,0,0,0,0,100,100,1,0,3,34,0,2,50,50,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(sec):
    h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def braces_to_cyan(text):
    # "{...}" in spec text marks the highlighted part.
    return re.sub(r"\{([^}]*)\}", lambda m: "{\\c" + CYAN + "}" + m.group(1) + "{\\c" + WHITE + "}", text)


def parse_srt(path):
    out = []
    for block in pathlib.Path(path).read_text().strip().split("\n\n"):
        lines = block.strip().split("\n")
        a, b = lines[1].split(" --> ")
        sec = lambda t: int(t[:2]) * 3600 + int(t[3:5]) * 60 + float(t[6:].replace(",", "."))
        out.append((sec(a), sec(b), " ".join(lines[2:])))
    return out


def inside(t, windows):
    return any(a <= t < b for a, b in windows)


def build_ass(spec, srt):
    ev = []
    hook = spec.get("hook")
    hook_until = hook["until"] if hook else 0
    if hook:
        ev.append(f"Dialogue: 1,{ts(0)},{ts(hook_until)},HookBox,,0,0,0,,{{\\fscx106\\fscy106\\t(0,120,\\fscx100\\fscy100)}}{hook['box']}")
        if hook.get("sub"):
            ev.append(f"Dialogue: 1,{ts(0.1)},{ts(hook_until)},HookSub,,0,0,0,,{{\\fad(80,0)}}{hook['sub']}")
    # the line spoken under the hook boxes gets one caption after them ("then")
    first_after = next((a for a, b, t in srt if a >= hook_until - 0.05), None)
    if hook and hook.get("then") and first_after:
        ev.append(f"Dialogue: 0,{ts(hook_until)},{ts(first_after - 0.05)},Cap,,0,0,0,,{POP}{braces_to_cyan(hook['then'])}")
    for p in spec.get("punches", []):
        style = "PunchTop" if p.get("pos") == "top" else "Punch"
        ev.append(f"Dialogue: 1,{ts(p['start'])},{ts(p['end'])},{style},,0,0,0,,{{\\fscx108\\fscy108\\t(0,120,\\fscx100\\fscy100)}}{braces_to_cyan(p['text'])}")
    reps, hl = spec.get("replace", {}), sorted(spec.get("highlight", []), key=len, reverse=True)
    no_caps = spec.get("no_captions", []) + [[p["start"], p["end"]] for p in spec.get("punches", [])]
    for a, b, text in srt:
        if a < hook_until - 0.05 or inside(a, no_caps):
            continue
        for k, v in reps.items():
            text = re.sub(re.escape(k), v, text, flags=re.I)
        for w in hl:
            text = re.sub(re.escape(w), lambda m: "{\\c" + CYAN + "}" + m.group(0) + "{\\c" + WHITE + "}", text, flags=re.I)
        style = "CapTop" if inside(a, spec.get("caption_top", [])) else "Cap"
        ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},{style},,0,0,0,,{POP}{text}")
    return HEADER + "\n".join(ev) + "\n"


def run(spec_path):
    sp = pathlib.Path(spec_path).resolve()
    spec = json.loads(sp.read_text())
    rel = lambda p: str(p if pathlib.Path(p).is_absolute() else (sp.parent / p).resolve())
    out = pathlib.Path(rel(spec["out"])); out.parent.mkdir(parents=True, exist_ok=True)
    ass = out.with_suffix(".ass"); ass.write_text(build_ass(spec, parse_srt(rel(spec["srt"]))))
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", rel(spec["avatar"])]).decode())

    inputs, chains = ["-i", rel(spec["avatar"])], []
    chains.append(f"[0:v]{'hflip,' if spec.get('hflip', True) else ''}scale=1080:1920,setsar=1[v0]")
    cur, n = "v0", 1
    for i, o in enumerate(spec.get("overlays", [])):
        lab = f"o{i}"
        if o["type"] == "broll":
            inputs += ["-i", rel(o["clip"])]
            sp_ = o.get("speed", 1.0)
            fit = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=25"
            if o.get("zoom"):
                chains.append(f"[{n}:v]trim={o['from']}:{o['to']},setpts=(PTS-STARTPTS)*{sp_},{fit},"
                              f"zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=25,setpts=PTS-STARTPTS+{o['at']}/TB[{lab}]")
            else:
                chains.append(f"[{n}:v]trim={o['from']}:{o['to']},setpts=(PTS-STARTPTS)*{sp_}+{o['at']}/TB,{fit}[{lab}]")
            end = o["at"] + (o["to"] - o["from"]) * sp_
            chains.append(f"[{cur}][{lab}]overlay=enable='between(t,{o['at']},{end:.2f})':eof_action=pass[c{i}]")
        elif o["type"] == "notif":
            inputs += ["-i", str(HERE / "assets/notif.webm")]
            chains.append(f"[{n}:v]setpts=PTS-STARTPTS,trim=start=0.3,setpts=PTS-STARTPTS+{o['at']}/TB,scale=1080:2337,crop=1080:1920:0:0,setsar=1,fps=25[{lab}]")
            chains.append(f"[{cur}][{lab}]overlay=enable='between(t,{o['at']},{o['until']})':eof_action=repeat[c{i}]")
        elif o["type"] == "image":
            inputs += ["-loop", "1", "-i", rel(o["src"])]
            chains.append(f"[{n}:v]format=rgba,trim=0:{dur + 0.1:.2f},fade=in:st={o['at']}:d=0.18:alpha=1,fade=out:st={o['until'] - 0.2:.2f}:d=0.2:alpha=1[{lab}]")
            chains.append(f"[{cur}][{lab}]overlay=enable='between(t,{o['at']},{o['until']})':shortest=1[c{i}]")
        else:
            sys.exit(f"unknown overlay type {o['type']}")
        cur, n = f"c{i}", n + 1
    fontsdir = str(FONTS).replace(":", "\\:")
    chains.append(f"[{cur}]subtitles={ass}:fontsdir={fontsdir},format=yuv420p[m]")
    if spec.get("endcard"):
        inputs += ["-i", rel(spec["endcard"])]
        chains.append(f"[{n}:v]setsar=1,format=yuv420p[e]")
        chains.append(f"[m][0:a][e][{n}:a]concat=n=2:v=1:a=1[v][a]")
        maps = ["-map", "[v]", "-map", "[a]"]
    else:
        maps = ["-map", "[m]", "-map", "0:a"]
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), *maps,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    # contact sheet for QA: one frame every 2s
    sheet = out.with_name(out.stem + "-sheet.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf", "fps=1/2,scale=180:-2,tile=8x2", "-frames:v", "1", str(sheet)], check=True)
    print(out, sheet)


if __name__ == "__main__":
    run(sys.argv[1])
