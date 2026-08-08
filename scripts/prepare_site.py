#!/usr/bin/env python3
"""Stage handbook Markdown for MkDocs without changing the source layout."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / ".site-docs"

ROOT_DOCUMENTS = (
    "SUMMARY.md",
    "GLOSSARY.md",
    "CROSS_REFERENCE_INDEX.md",
    "PRODUCTION_PLAYBOOK.md",
    "INTERVIEW_PLAYBOOK.md",
    "HANDBOOK_COVERAGE.md",
    "SPECIFICATION.md",
)


def reset_destination() -> None:
    if DESTINATION.parent != ROOT or DESTINATION.name != ".site-docs":
        raise RuntimeError("Refusing to clear an unexpected staging directory")
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.mkdir()


def copy_markdown_tree(source: Path, destination: Path) -> None:
    for markdown in sorted(source.rglob("*.md")):
        relative = markdown.relative_to(source)
        if relative.name == "README.md":
            relative = relative.with_name("index.md")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(markdown, target)


def mark_search_excluded(markdown: Path) -> None:
    """Exclude supporting/reference pages from the client-side full-text index."""
    content = markdown.read_text(encoding="utf-8")
    metadata = "search:\n  exclude: true\n"
    if content.startswith("---\n"):
        closing = content.find("\n---\n", 4)
        if closing == -1:
            raise RuntimeError(f"Unclosed front matter in {markdown}")
        content = content[:closing] + "\n" + metadata + content[closing:]
    else:
        content = f"---\n{metadata}---\n\n{content}"
    markdown.write_text(content, encoding="utf-8")


def main() -> None:
    reset_destination()

    shutil.copy2(ROOT / "README.md", DESTINATION / "index.md")
    for filename in ROOT_DOCUMENTS:
        shutil.copy2(ROOT / filename, DESTINATION / filename)

    for phase in sorted(ROOT.glob("Phase-*")):
        if phase.is_dir():
            copy_markdown_tree(phase, DESTINATION / phase.name)

    copy_markdown_tree(ROOT / "templates", DESTINATION / "handbook-templates")
    shutil.copytree(ROOT / "assets", DESTINATION / "assets", dirs_exist_ok=True)
    for readme in sorted((DESTINATION / "assets").rglob("README.md")):
        readme.rename(readme.with_name("index.md"))

    mark_search_excluded(DESTINATION / "SPECIFICATION.md")
    mark_search_excluded(DESTINATION / "HANDBOOK_COVERAGE.md")
    for template in sorted((DESTINATION / "handbook-templates").glob("*.md")):
        mark_search_excluded(template)

    # MkDocs reserves a top-level `templates/` directory for theme templates.
    # The source layout remains unchanged; only staged links use another name.
    for markdown in sorted(DESTINATION.rglob("*.md")):
        content = markdown.read_text(encoding="utf-8")
        content = content.replace("(templates/", "(handbook-templates/")
        content = content.replace("(../templates/", "(../handbook-templates/")
        markdown.write_text(content, encoding="utf-8")

    page_count = len(list(DESTINATION.rglob("*.md")))
    print(f"Prepared {page_count} Markdown pages in {DESTINATION.name}")


if __name__ == "__main__":
    main()
