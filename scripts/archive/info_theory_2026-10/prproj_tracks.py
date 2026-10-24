"""Which media each timeline track item uses in a Premiere .prproj, plus its Mute / Volume and the
Lumetri values that differ from the default. Follows ObjectRef / ObjectURef links from each
*ClipTrackItem down to the Media element with a FilePath. Read-only, ~1 s per file.

    python prproj_tracks.py <file.prproj> [...]
"""
import collections
import gzip
import sys
import xml.etree.ElementTree as ET

TICKS = 254016000000


def build_index(root):
    idx = {}
    for el in root.iter():
        for key in ("ObjectID", "ObjectUID"):
            if key in el.attrib:
                idx[el.attrib[key]] = el
    return idx


def find_media(el, idx, seen=None, depth=0):
    """Return the set of media file paths reachable from el through object references."""
    seen = seen if seen is not None else set()
    found = set()
    if depth > 12:
        return found
    for sub in el.iter():
        if sub.tag in ("FilePath", "ActualMediaFilePath") and sub.text:
            found.add(sub.text.rsplit("\\", 1)[-1])
        for key in ("ObjectRef", "ObjectURef"):
            ref = sub.attrib.get(key)
            if ref and ref not in seen and ref in idx:
                seen.add(ref)
                found |= find_media(idx[ref], idx, seen, depth + 1)
    return found


for path in sys.argv[1:]:
    root = ET.fromstring(gzip.open(path).read())
    idx = build_index(root)
    print(f"=== {path}")
    counts = collections.Counter()
    for kind in ("VideoClipTrackItem", "AudioClipTrackItem"):
        for item in root.iter(kind):
            ci = item.find("ClipTrackItem/TrackItem")
            start = end = None
            if ci is not None:
                s, e = ci.findtext("Start"), ci.findtext("End")
                start = int(s) / TICKS if s else 0.0
                end = int(e) / TICKS if e else None
            media = find_media(item, idx)
            counts[(kind, tuple(sorted(media)))] += 1
            if end is not None:
                print(f"  {kind[:5]} {start:8.1f}-{end:8.1f} s  {sorted(media)}")
    print("summary:", dict(counts))
    # Lumetri / volume parameters: name -> values seen
    params = collections.defaultdict(set)
    for p in root.iter():
        name = p.findtext("Name")
        if name in {"Exposure", "Contrast", "Highlights", "Shadows", "Whites", "Blacks", "Saturation",
                    "Temperature", "Volume", "Mute", "Level", "Make-Up Gain", "Amount"}:
            val = p.findtext("CurrentValue") or p.findtext("StartKeyframe")
            if val is not None:
                params[name].add(val.split(",")[1] if "," in val else val)
    print("params:", {k: sorted(v)[:6] for k, v in params.items()})
