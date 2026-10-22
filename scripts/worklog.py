#!/usr/bin/env python3
"""Read and append to the project worklog.

The worklog rots when writing an entry costs more than skipping it. This keeps the cost to one
command, and makes staleness visible instead of silent.

    worklog.py status              show the state block and a staleness check
    worklog.py add                 append an entry (flags or interactive prompts)

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import List, Optional

DEFAULT_WORKLOG = Path("project/worklog.md")
STATE_RE = re.compile(r"^## Current state\s*\n(.*?)(?=^---|\Z)", re.DOTALL | re.M)
UPDATED_RE = re.compile(r"^\s*-\s*\*\*Updated:\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)
STAGE_RE = re.compile(r"^\s*-\s*\*\*Stage:\*\*\s*(.+?)\s*$", re.M)
DRAFT_RE = re.compile(r"^\s*-\s*\*\*Draft file:\*\*\s*(.+?)\s*$", re.M)
ENTRY_DATE_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2})", re.M)

STALE_DAYS = 21


def read_worklog(path: Path) -> str:
    if not path.is_file():
        print(f"error: no worklog at {path}", file=sys.stderr)
        print("hint: copy project/_TEMPLATE/worklog.md into project/", file=sys.stderr)
        raise SystemExit(2)
    return path.read_text(encoding="utf-8")


def state_block(text: str) -> str:
    match = STATE_RE.search(text)
    if match is None:
        return ""
    lines = [ln for ln in match.group(1).splitlines() if ln.strip() and not ln.strip().startswith("<!--")]
    return "\n".join(lines)


def parse_date(raw: Optional[str]) -> Optional[dt.date]:
    if not raw:
        return None
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        return None


def staleness_report(path: Path, text: str, today: dt.date) -> List[str]:
    """Compare the worklog's own date against entries and the draft's mtime."""
    notes: List[str] = []

    updated = parse_date(match.group(1) if (match := UPDATED_RE.search(text)) else None)
    if updated is None:
        notes.append("State block has no valid **Updated:** date — treat it as unverified.")
    else:
        age = (today - updated).days
        if age > STALE_DAYS:
            notes.append(f"State block is {age} days old (updated {updated}). Confirm before relying on it.")

    entry_dates = [parse_date(d) for d in ENTRY_DATE_RE.findall(text)]
    entry_dates = [d for d in entry_dates if d is not None]
    if entry_dates and updated is not None and max(entry_dates) > updated:
        notes.append(
            f"Newest entry ({max(entry_dates)}) is later than the state block ({updated}). "
            "The state block was probably not refreshed."
        )

    draft_raw = match.group(1).strip() if (match := DRAFT_RE.search(text)) else ""
    draft_raw = draft_raw.strip("`")
    if draft_raw and not draft_raw.startswith("<!--"):
        draft = resolve_draft(path, draft_raw)
        if draft is not None:
            mtime = dt.date.fromtimestamp(draft.stat().st_mtime)
            if updated is not None and mtime > updated:
                notes.append(
                    f"Draft {draft_raw} was modified {mtime}, after the state block ({updated}). "
                    "The worklog may not reflect the current draft."
                )
        else:
            notes.append(f"Draft file named in the state block was not found: {draft_raw}")
    return notes


def resolve_draft(worklog: Path, raw: str) -> Optional[Path]:
    """Find the draft named in the state block.

    The path may be written relative to the working directory, the bundle root, or the
    repository that contains the bundle, so try each in turn.
    """
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate if candidate.is_file() else None
    bundle = worklog.resolve().parent.parent
    for base in (Path.cwd(), worklog.parent, bundle, bundle.parent):
        resolved = base / candidate
        if resolved.is_file():
            return resolved
    return None


def cmd_status(args: argparse.Namespace) -> int:
    text = read_worklog(args.worklog)
    block = state_block(text)
    print(f"Worklog: {args.worklog}\n")
    print(block if block else "(no Current state block found)")
    notes = staleness_report(args.worklog, text, dt.date.today())
    print("\nStaleness check:")
    if notes:
        for note in notes:
            print(f"- {note}")
        return 1
    print("- State block looks current.")
    return 0


def prompt(label: str, supplied: Optional[str]) -> str:
    if supplied is not None:
        return supplied
    if not sys.stdin.isatty():
        return ""
    try:
        return input(f"{label}: ").strip()
    except EOFError:
        return ""


def cmd_add(args: argparse.Namespace) -> int:
    text = read_worklog(args.worklog)
    date = args.date or dt.date.today().isoformat()
    label = prompt("Short label", args.label) or "session"
    entry = [
        f"\n### {date} — {label}\n",
        f"- **Stage:** {prompt('Stage (e.g. 5 -> 6)', args.stage) or 'unchanged'}",
        f"- **Did:** {prompt('Did', args.did)}",
        f"- **Decided:** {prompt('Decided', args.decided) or 'nothing new'}",
        f"- **Open:** {prompt('Open', args.open) or 'nothing new'}",
        f"- **AI:** {prompt('AI assistance', args.ai) or 'none'}",
        "",
    ]
    with args.worklog.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(entry))
    print(f"Appended entry dated {date} to {args.worklog}")
    print("Remember to refresh the Current state block — it is what gets read first.")
    if args.ai and args.ai != "none":
        print("This entry records AI assistance; mirror it into the venue's AI-use log.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read and append to the project worklog.")
    parser.add_argument("--worklog", type=Path, default=DEFAULT_WORKLOG,
                        help=f"path to the worklog (default: {DEFAULT_WORKLOG})")
    sub = parser.add_subparsers(dest="command", required=True)

    # Accept --worklog on either side of the subcommand; SUPPRESS keeps the
    # subparser from overwriting a value given before it.
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--worklog", type=Path, default=argparse.SUPPRESS,
                        help=f"path to the worklog (default: {DEFAULT_WORKLOG})")

    status = sub.add_parser("status", parents=[shared],
                            help="show the state block and a staleness check")
    status.set_defaults(func=cmd_status)

    add = sub.add_parser("add", parents=[shared], help="append a dated entry")
    add.add_argument("--date", help="ISO date (default: today)")
    add.add_argument("--label")
    add.add_argument("--stage")
    add.add_argument("--did")
    add.add_argument("--decided")
    add.add_argument("--open")
    add.add_argument("--ai")
    add.set_defaults(func=cmd_add)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
