"""Two Robots in an Elevator - make.fun bounty entry.

Writes exactly one original funny line about two robots stuck in an
elevator to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), with no
trailing newline. Validates the line before writing, then reads the
file back and re-validates the exact bytes on disk.

Pure Python standard library only.
"""

import os

LINE = (
    'Robot one whispered, "Don\'t panic, I know every floor," '
    'and robot two replied, "Great, then tell the doors," '
    "and the elevator stayed silent."
)


def validate_line(line: str) -> None:
    """Check the entry line against the competition's rules.

    Validates the exact characters of the line: it must be a single
    printable-ASCII line, between 20 and 200 characters, with no tabs,
    no control characters, no double spaces, and it must end with a
    period. Raises ValueError on the first failing check.
    """
    if not line:
        raise ValueError("line is empty")
    if len(line) < 20:
        raise ValueError(f"line is {len(line)} chars, under the 20 minimum")
    if len(line) > 200:
        raise ValueError(f"line is {len(line)} chars, over the 200 limit")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if "\t" in line:
        raise ValueError("line contains a tab character")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line contains a control character")
    if any(ord(ch) > 0x7E for ch in line):
        raise ValueError("line contains a non-ASCII character")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "  " in line:
        raise ValueError("line contains double spaces")
    if not line.endswith("."):
        raise ValueError("line must end with a period")


def main() -> None:
    validate_line(LINE)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        raise ValueError("read-back mismatch: bytes on disk differ")
    validate_line(on_disk.decode("utf-8"))

    print(f"Wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
