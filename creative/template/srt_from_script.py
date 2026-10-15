#!/usr/bin/env python3
"""Make a caption SRT whose words come from the script and whose timing comes from a transcription.

HeyGen gives no caption file for non-English voices, and speech-to-text mishears words
(e.g. "kurenje" for "curenje"). So: take the transcription SRT (Arcads arcads_transcribe,
format "srt") for timing only, and pour the script's words into its cues in order.

Usage: python3 srt_from_script.py script.txt transcription.srt out.srt
Words are matched by count per cue, so the transcription must have about as many words as
the script (check the printed word counts; a big mismatch means re-render or fix by hand).
"""
import pathlib, re, sys


def cues(path):
    out = []
    for block in pathlib.Path(path).read_text().strip().split("\n\n"):
        lines = block.strip().split("\n")
        a, b = lines[1].split(" --> ")
        out.append([a.strip(), b.strip(), " ".join(lines[2:]).split()])
    return out


def main(script, srt, dest):
    words = pathlib.Path(script).read_text().split()
    cs = cues(srt)
    n_t = sum(len(c[2]) for c in cs)
    print(f"script words {len(words)}, transcription words {n_t}")
    # spread script words over the cues in proportion to each cue's transcribed word count
    out, i = [], 0
    for k, (a, b, w) in enumerate(cs):
        take = round(len(w) * len(words) / n_t) if k < len(cs) - 1 else len(words) - i
        take = max(1, min(take, len(words) - i - (len(cs) - k - 1)))
        out.append((a, b, " ".join(words[i:i + take])))
        i += take
    pathlib.Path(dest).write_text("\n".join(f"{n}\n{a} --> {b}\n{t}\n" for n, (a, b, t) in enumerate(out, 1)))
    for a, b, t in out:
        print(a, t)


if __name__ == "__main__":
    main(*sys.argv[1:4])
