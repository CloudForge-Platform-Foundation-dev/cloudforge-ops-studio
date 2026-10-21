"""Fail CI if a git-tracked text file is not UTF-8 without BOM.

Prints only file names and the kind of problem; never file contents.
Binary files are skipped by suffix (extend SKIP_SUFFIX if you add new binary assets).
"""
import pathlib
import subprocess
import sys

SKIP_SUFFIX = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz",
    ".woff", ".woff2", ".ttf", ".otf", ".whl", ".pyc",
}


def classify(data):
    if data.startswith(b"\xff\xfe"):
        return "utf-16-le-bom"
    if data.startswith(b"\xfe\xff"):
        return "utf-16-be-bom"
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-bom"
    if b"\x00" in data:
        return "contains-nul-bytes"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return "invalid-utf-8"
    return None


def main():
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    raw = subprocess.check_output(["git", "-C", root, "ls-files", "-z"])
    bad = []
    for rel in raw.decode("utf-8").split("\0"):
        if not rel:
            continue
        path = pathlib.Path(root) / rel
        if path.suffix.lower() in SKIP_SUFFIX or not path.is_file():
            continue
        kind = classify(path.read_bytes())
        if kind:
            bad.append((kind, rel))
    for kind, rel in bad:
        print(f"{kind:20} {rel}")
    if bad:
        print(f"FAILED: {len(bad)} file(s) are not UTF-8 without BOM")
        sys.exit(1)
    print("OK: all tracked text files are UTF-8 without BOM")


if __name__ == "__main__":
    main()
