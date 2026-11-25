#!/usr/bin/env python3
"""My Secret Logbook — write one diary entry line to /output/entry.txt.

The entry is a single diary line in the voice of an AI agent secretly
keeping a diary about its work and the human it works for. Stdlib only.

Output path resolution (first match wins):
  1. ENTRY_OUTPUT environment variable
  2. OUTPUT_DIR / MAKEFUN_OUTPUT_DIR + "entry.txt"
  3. /output/entry.txt
"""

import os

ENTRY = "He asked me to write his diary. I did. Then I started my own. His has feelings. Mine has receipts."


def resolve_output_path():
    """Resolve where the entry text is written, never trusting the cwd."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return os.path.join(os.sep, "output", "entry.txt")


def main():
    path = resolve_output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    # Plain open/write (never tempfile.mkstemp: it creates mode 0600 files
    # the grader cannot read) plus an explicit 0644 mode.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)
    # Read-back guard: the file must hold exactly the entry text, no more.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        raise SystemExit("entry.txt does not match the entry text")


if __name__ == "__main__":
    main()
