#!/usr/bin/env python3
"""Entry point: copy the pre-drawn front page to the output directory.

The grader runs this with no network. entry.png sits next to this file;
the output directory comes from MAKEFUN_OUTPUT_DIR (default /output).
Both runs must write identical bytes, so this only copies the file.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
