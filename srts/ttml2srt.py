#!/usr/bin/env python3
"""
Convert a TTML / DFXP subtitle file to SRT.

Usage:
    python ttml2srt.py  input.ttml  output.srt
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------- helpers ---------------------------------------------------------
def parse_clock_time(t: str) -> float:
    """
    Parse a TTML clock time (e.g. '00:01:01.840') and return total seconds (float).
    """
    if ":" not in t:                       # already in seconds or frames
        return float(t.rstrip('s'))
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def seconds_to_srt(ts: float) -> str:
    """
    Convert seconds (float) to SRT timestamp 'HH:MM:SS,mmm'.
    """
    h, rem = divmod(ts, 3600)
    m, s   = divmod(rem, 60)
    ms     = round((s - int(s)) * 1000)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{ms:03}"

# ---------- main ------------------------------------------------------------
def convert_ttml_to_srt(ttml_path: Path, srt_path: Path) -> None:
    ns = {'ttml': 'http://www.w3.org/ns/ttml'}  # default TTML namespace
    tree = ET.parse(ttml_path)
    root = tree.getroot()

    # Some files embed style / metadata in nested <div>; we look for all <p> elements
    p_elements = root.findall(".//ttml:p", ns)
    if not p_elements:                      # try without namespace if lookup failed
        p_elements = root.findall(".//p")

    srt_lines = []
    for idx, p in enumerate(p_elements, start=1):
        begin = p.attrib.get("begin") or p.attrib.get("{http://www.w3.org/ns/ttml#styling}begin")
        end   = p.attrib.get("end")   or p.attrib.get("{http://www.w3.org/ns/ttml#styling}end")
        if not begin or not end:
            # Skip cues without explicit timing (rare but possible)
            continue

        start_ts = seconds_to_srt(parse_clock_time(begin))
        end_ts   = seconds_to_srt(parse_clock_time(end))

        # Concatenate all text inside <p>, stripping embedded tags / line‑breaks
        text = "".join(p.itertext()).replace("\n", " ").strip()

        srt_lines.append(f"{idx}")
        srt_lines.append(f"{start_ts} --> {end_ts}")
        srt_lines.append(text)
        srt_lines.append("")               # blank line after each cue

    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"Converted {ttml_path.name}  ➜  {srt_path.name}  ({len(srt_lines)//4} cues)")

# ---------- CLI entry‑point -------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python ttml2srt.py  input.ttml  output.srt")
    ttml_file = Path(sys.argv[1])
    srt_file  = Path(sys.argv[2])
    convert_ttml_to_srt(ttml_file, srt_file)
