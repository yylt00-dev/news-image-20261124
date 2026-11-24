#!/usr/bin/env python3
"""Run the entry: put the finished front page where the grader looks.

The picture itself is drawn ahead of time by draw_front.py and shipped
as entry.png next to this file, so running the entry needs no network
and always produces the same bytes. The grader sets MAKEFUN_OUTPUT_DIR;
without it, the image goes to /output.
"""

import os
import shutil
from pathlib import Path


def run() -> Path:
    here = Path(__file__).resolve().parent
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(here / "entry.png", target)
    return target


if __name__ == "__main__":
    done = run()
    print(f"wrote {done} ({done.stat().st_size} bytes)")
