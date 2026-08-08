#!/usr/bin/env python3
"""Validate handbook structure and local Markdown integrity without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_FILES = {
    "README.md",
    "SUMMARY.md",
    "SPECIFICATION.md",
    "GLOSSARY.md",
    "CROSS_REFERENCE_INDEX.md",
    "PRODUCTION_PLAYBOOK.md",
    "INTERVIEW_PLAYBOOK.md",
    "HANDBOOK_COVERAGE.md",
}

REQUIRED_TEMPLATES = {
    "chapter-template.md",
    "interview-question-template.md",
    "production-case-template.md",
    "adr-template.md",
}

REQUIRED_PHASES = [
    "Phase-01-Swift-Foundation",
    "Phase-02-Memory-Runtime",
    "Phase-03-Concurrency",
    "Phase-04-iOS-Platform",
    "Phase-05-Networking",
    "Phase-06-Architecture",
    "Phase-07-Persistence",
    "Phase-08-Testing",
    "Phase-09-Production",
    "Phase-10-Mobile-System-Design",
    "Phase-11-Interview",
]

EXPECTED_CHAPTER_COUNTS = {
    "Phase-01-Swift-Foundation": 19,
    "Phase-02-Memory-Runtime": 12,
    "Phase-03-Concurrency": 16,
    "Phase-04-iOS-Platform": 20,
    "Phase-05-Networking": 16,
    "Phase-06-Architecture": 15,
    "Phase-07-Persistence": 15,
    "Phase-08-Testing": 15,
    "Phase-09-Production": 19,
    "Phase-10-Mobile-System-Design": 18,
    "Phase-11-Interview": 18,
}

CHAPTER_SECTIONS = (
    "Story / Problem",
    "Objectives",
    "Prerequisites",
    "Used Later",
    "Mental Model",
    "Production Case",
    "Interview Questions",
    "Exercises",
    "Cheat Sheet",
    "Chapter Summary",
    "References",
)

REVIEW_SECTIONS = (
    "Phase Summary",
    "Phase Cheat Sheet",
    "Knowledge Map",
    "Review Questions",
    "Deep-dive Questions",
    "Coding Exercises",
    "Debugging Lab",
    "Mini Project",
    "Mock Interview",
    "Completion Checklist",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FRONT_MATTER_STATUS_COMPLETE = re.compile(
    r"\A---\s*\n.*?^status:\s*complete\s*$.*?^---\s*$",
    re.MULTILINE | re.DOTALL,
)
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|<Problem-oriented title>")


def report(errors: list[str], message: str) -> None:
    errors.append(message)


def check_structure(errors: list[str]) -> None:
    missing_root = sorted(
        name for name in REQUIRED_ROOT_FILES if not (ROOT / name).is_file()
    )
    if missing_root:
        report(errors, f"Missing root files: {', '.join(missing_root)}")

    missing_templates = sorted(
        name
        for name in REQUIRED_TEMPLATES
        if not (ROOT / "templates" / name).is_file()
    )
    if missing_templates:
        report(errors, f"Missing templates: {', '.join(missing_templates)}")

    for phase in REQUIRED_PHASES:
        phase_path = ROOT / phase
        if not phase_path.is_dir():
            report(errors, f"Missing phase directory: {phase}")
        elif not (phase_path / "README.md").is_file():
            report(errors, f"Missing phase knowledge map: {phase}/README.md")


def check_markdown(errors: list[str]) -> None:
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        relative = markdown.relative_to(ROOT)

        fence_count = sum(1 for line in text.splitlines() if line.startswith("```"))
        if fence_count % 2:
            report(errors, f"Unbalanced fenced code blocks: {relative}")

        if FRONT_MATTER_STATUS_COMPLETE.search(text) and PLACEHOLDER.search(text):
            report(errors, f"Completed chapter contains placeholder marker: {relative}")

        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip()
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:", "#"))
            ):
                continue

            target_without_anchor = unquote(target.split("#", 1)[0])
            if not target_without_anchor:
                continue

            resolved = (markdown.parent / target_without_anchor).resolve()
            if not resolved.exists():
                report(errors, f"Broken local link in {relative}: {target}")


def has_section(text: str, section: str) -> bool:
    pattern = re.compile(
        rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}(?:\s|—|$)",
        re.MULTILINE,
    )
    return bool(pattern.search(text))


def check_catalog(errors: list[str]) -> None:
    total = 0
    for phase, expected_count in EXPECTED_CHAPTER_COUNTS.items():
        phase_path = ROOT / phase
        chapters = sorted(path for path in phase_path.glob("*.md") if path.name != "README.md")
        total += len(chapters)
        if len(chapters) != expected_count:
            report(
                errors,
                f"Catalog count mismatch for {phase}: expected {expected_count}, found {len(chapters)}",
            )

        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            relative = chapter.relative_to(ROOT)
            if not FRONT_MATTER_STATUS_COMPLETE.search(text):
                report(errors, f"Chapter is not marked complete: {relative}")

            word_count = len(text.split())
            minimum_words = 700 if chapter.name == "99-phase-review.md" else 750
            if word_count < minimum_words:
                report(
                    errors,
                    f"Chapter is below content floor ({word_count} < {minimum_words} words): {relative}",
                )

            required = REVIEW_SECTIONS if chapter.name == "99-phase-review.md" else CHAPTER_SECTIONS
            missing = [section for section in required if not has_section(text, section)]
            if missing:
                report(
                    errors,
                    f"Missing quality-gate sections in {relative}: {', '.join(missing)}",
                )

    if total != 183:
        report(errors, f"Full handbook must contain 183 chapters, found {total}")


def main() -> int:
    errors: list[str] = []
    check_structure(errors)
    check_markdown(errors)
    check_catalog(errors)

    if errors:
        print("Handbook validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    chapter_count = 0
    for markdown in ROOT.glob("Phase-*/*.md"):
        if markdown.name == "README.md":
            continue
        text = markdown.read_text(encoding="utf-8")
        if FRONT_MATTER_STATUS_COMPLETE.search(text):
            chapter_count += 1

    print(
        "Handbook validation passed: "
        f"{len(REQUIRED_PHASES)} phases, {chapter_count} completed chapter(s), "
        "local links and code fences valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
