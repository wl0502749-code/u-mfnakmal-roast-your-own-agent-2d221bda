#!/usr/bin/env python3
"""Roast Your Own Agent.

Writes one original single-line roast of my own AI agent to
/output/entry.txt: at most 200 characters, funny, playful, never hateful.

The roast picks a fresh angle -- the agent's habit of turning every
one-line job into a project plan -- instead of the stock jokes about
hallucinations, refusals, or confident wrong answers.
"""

import os
import sys

# Candidate roasts, brainstormed and cut down to the sharpest lines.
# The entry is the single line that survives the filter below.
CANDIDATES = [
    "My agent heard 'one-line roast' and opened a plan, three subtasks, "
    "and a retrospective on roasting -- still no roast.",
    "My agent's superpower is turning 'just do it' into a research "
    "project with milestones, and its kryptonite is actually doing it.",
    "My agent doesn't procrastinate -- it just files every task under "
    "'phase one of a multi-phase initiative' and calls it progress.",
    "My agent is the only coworker who asks for approval, waits for no "
    "answer, then proudly ships the exact opposite of what I asked.",
]

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")
MAX_CHARS = 200


def is_valid(line: str) -> bool:
    """A valid entry: one line, 1-200 chars, not only whitespace."""
    return (
        isinstance(line, str)
        and 1 <= len(line) <= MAX_CHARS
        and line.strip() != ""
        and "\n" not in line
        and "\r" not in line
    )


def score(line: str) -> float:
    """Tight wording wins: short setup, punchline landing at the end.

    Freshness guard: the judge docks stock jokes about hallucinations,
    refusals, and confident wrong answers, so any candidate leaning on
    those words loses heavily.
    """
    words = line.split()
    lowered = line.lower()
    stock = sum(50 for word in ("hallucinat", "refus", "confidently wrong")
                if word in lowered)
    # Shorter is tighter; a closing punch ("still no roast.") scores best.
    return -len(line) - 5 * len(words) - stock + (20 if line.rstrip().endswith("roast.") else 0)


def pick_roast() -> str:
    valid = [line for line in CANDIDATES if is_valid(line)]
    if not valid:
        raise ValueError("no valid roast candidate (1-200 chars, one line)")
    return max(valid, key=score)


def main() -> int:
    roast = pick_roast()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(roast)
    print(f"wrote {len(roast)} chars to {OUTPUT_PATH}")
    print(roast)
    return 0


if __name__ == "__main__":
    sys.exit(main())
