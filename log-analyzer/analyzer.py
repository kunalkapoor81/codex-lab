from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable
import re

LOG_LEVELS = ("ERROR", "WARNING", "INFO")
TIMESTAMP_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})")


def read_log_lines(log_path: Path) -> list[str]:
    """Read all lines from the log file."""
    return log_path.read_text(encoding="utf-8").splitlines()


def count_log_levels(lines: Iterable[str]) -> Counter:
    """Count ERROR, WARNING, and INFO entries in the log lines."""
    counts: Counter = Counter({level: 0 for level in LOG_LEVELS})
    for line in lines:
        for level in LOG_LEVELS:
            if level in line:
                counts[level] += 1
                break
    return counts


def extract_error_timestamps(lines: Iterable[str]) -> list[str]:
    """Extract timestamps from lines that contain ERROR."""
    timestamps: list[str] = []
    for line in lines:
        if "ERROR" not in line:
            continue

        match = TIMESTAMP_PATTERN.match(line.strip())
        if match:
            timestamps.append(match.group(1))
        else:
            timestamps.append("<timestamp not found>")

    return timestamps


def build_report(counts: Counter, error_timestamps: list[str]) -> str:
    """Build report text for writing to report.txt."""
    header = "Log Analysis Summary"
    divider = "=" * len(header)

    timestamps_text = "\n".join(f"- {ts}" for ts in error_timestamps) or "- None"

    return (
        f"{header}\n"
        f"{divider}\n\n"
        f"Counts:\n"
        f"- ERROR: {counts['ERROR']}\n"
        f"- WARNING: {counts['WARNING']}\n"
        f"- INFO: {counts['INFO']}\n\n"
        f"Error Timestamps:\n"
        f"{timestamps_text}\n"
    )


def generate_summary(log_path: Path, report_path: Path) -> None:
    """Generate log summary report from the input log file."""
    lines = read_log_lines(log_path)
    counts = count_log_levels(lines)
    error_timestamps = extract_error_timestamps(lines)
    report = build_report(counts, error_timestamps)
    report_path.write_text(report, encoding="utf-8")
