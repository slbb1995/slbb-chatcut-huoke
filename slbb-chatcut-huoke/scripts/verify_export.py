#!/usr/bin/env python3
"""Read-only technical export verification; does not check caption pixels or sound quality."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def verify(path, expected_duration=None, decode=False, *, expected_width=1080,
           expected_height=1920, expected_fps=30, expected_codec="h264"):
    if (expected_width <= 0 or expected_height <= 0 or
            not math.isfinite(expected_fps) or expected_fps <= 0 or not expected_codec.strip()):
        raise ValueError("Expected dimensions, fps and codec must be valid positive values/nonempty text")
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("Nonempty video file required")
    if not shutil.which("ffprobe"):
        raise ValueError("ffprobe unavailable")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise ValueError("ffprobe could not read the media")
    info = json.loads(r.stdout)
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    a = next((s for s in streams if s.get("codec_type") == "audio"), {})
    errors = []
    if v.get("codec_name") != expected_codec:
        errors.append("video codec is not " + expected_codec)
    if (v.get("width"), v.get("height")) != (expected_width, expected_height):
        errors.append("resolution is not %sx%s" % (expected_width, expected_height))
    try:
        fps = float(Fraction(v.get("avg_frame_rate", "0/1")))
    except (ValueError, ZeroDivisionError):
        fps = 0
    if abs(fps - expected_fps) > 0.01:
        errors.append("frame rate is not %sfps" % expected_fps)
    if not a:
        errors.append("audio stream missing")
    duration = float(info.get("format", {}).get("duration", 0))
    if not math.isfinite(duration) or duration <= 0:
        errors.append("invalid duration")
    if expected_duration is not None:
        if not math.isfinite(expected_duration) or expected_duration <= 0:
            raise ValueError("Expected duration must be a positive finite number")
        tolerance = max(2/expected_fps, 0.1)
        if abs(duration - expected_duration) > tolerance:
            errors.append("duration differs from main-track duration by more than %.3fs" % tolerance)
        for key, s in (("video", v), ("audio", a)):
            if s.get("duration") is not None:
                sd = float(s["duration"])
                if abs(sd - expected_duration) > tolerance:
                    errors.append(key + " stream duration differs from main track")
    fmt = info.get("format", {}).get("format_name", "")
    if "mp4" not in fmt.split(","):
        errors.append("container is not MP4-compatible")
    decoded = False
    if decode:
        if not shutil.which("ffmpeg"):
            raise ValueError("ffmpeg unavailable for decode check")
        timeout = max(60, min(3600, duration*10+30))
        d = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0",
                            "-map", "0:a:0?", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=timeout)
        decoded = d.returncode == 0 and not d.stderr.strip()
        if not decoded:
            errors.append("full decode reported an error")
    return {"technical_pass": not errors, "file": str(path.resolve()), "duration_seconds": duration,
            "expected": {"width": expected_width, "height": expected_height,
                         "fps": expected_fps, "codec": expected_codec},
            "codec": v.get("codec_name"), "width": v.get("width"), "height": v.get("height"),
            "fps": fps, "audio_present": bool(a), "decode_checked": decode, "decode_pass": decoded if decode else None,
            "errors": errors, "unverified": ["caption accuracy and pixels", "picture quality and sync", "audible mix and clipping"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", type=Path)
    ap.add_argument("--expected-duration", type=float)
    ap.add_argument("--expected-width", type=int, default=1080)
    ap.add_argument("--expected-height", type=int, default=1920)
    ap.add_argument("--expected-fps", type=float, default=30)
    ap.add_argument("--expected-codec", default="h264", help="ffprobe codec name; default: h264")
    ap.add_argument("--decode", action="store_true")
    args = ap.parse_args()
    try:
        result = verify(args.file.expanduser(), args.expected_duration, args.decode,
                        expected_width=args.expected_width, expected_height=args.expected_height,
                        expected_fps=args.expected_fps, expected_codec=args.expected_codec)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["technical_pass"] else 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"technical_pass": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
