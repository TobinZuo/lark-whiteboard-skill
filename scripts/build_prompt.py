#!/usr/bin/env python3
"""Build a diagram-specific SVG generation prompt from the prompt library."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_LIBRARY = ROOT / "references" / "prompt-library.md"
LAYOUT_RECIPES = ROOT / "references" / "layout-recipes.md"
LAYOUT_ARCHETYPES = ROOT / "references" / "layout-archetypes.md"

SECTION_BY_TYPE = {
    "architecture": "Architecture Prompt",
    "system-architecture": "Architecture Prompt",
    "service-architecture": "Architecture Prompt",
    "component": "Component Prompt",
    "component-diagram": "Component Prompt",
    "deployment": "Deployment Topology Prompt",
    "topology": "Deployment Topology Prompt",
    "infrastructure": "Deployment Topology Prompt",
    "data-flow": "Data Flow Prompt",
    "dfd": "Data Flow Prompt",
    "flowchart": "Flowchart Or Process Prompt",
    "process": "Flowchart Or Process Prompt",
    "pipeline": "CI/CD Pipeline Prompt",
    "ci-cd": "CI/CD Pipeline Prompt",
    "cicd": "CI/CD Pipeline Prompt",
    "swimlane": "Swimlane Prompt",
    "sequence": "Sequence Prompt",
    "api-sequence": "Sequence Prompt",
    "state-machine": "State Machine Prompt",
    "state": "State Machine Prompt",
    "erd": "ER Diagram Prompt",
    "er": "ER Diagram Prompt",
    "data-model": "ER Diagram Prompt",
    "org-chart": "Org Chart Prompt",
    "org": "Org Chart Prompt",
    "timeline": "Timeline Prompt",
    "mind-map": "Mind Map Prompt",
    "mindmap": "Mind Map Prompt",
    "matrix": "Matrix Prompt",
    "funnel": "Funnel Prompt",
}

RECIPE_BY_SECTION = {
    "Architecture Prompt": "Architecture Recipe",
    "Component Prompt": "Component Recipe",
    "Deployment Topology Prompt": "Deployment Recipe",
    "Data Flow Prompt": "Data Flow Recipe",
    "Flowchart Or Process Prompt": "Flowchart Recipe",
    "CI/CD Pipeline Prompt": "CI/CD Pipeline Recipe",
    "Swimlane Prompt": "Swimlane Recipe",
    "Sequence Prompt": "Sequence Recipe",
    "State Machine Prompt": "State Machine Recipe",
    "ER Diagram Prompt": "ER Diagram Recipe",
    "Org Chart Prompt": "Org Chart Recipe",
    "Timeline Prompt": "Timeline Recipe",
    "Mind Map Prompt": "Mind Map Recipe",
    "Matrix Prompt": "Matrix Recipe",
    "Funnel Prompt": "Funnel Recipe",
}

COMMON_RECIPE_HEADINGS = ["Layout Rule", "Canvas", "Node Dimensions", "Spacing", "Palette", "Typography"]


def extract_text_block(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$.*?```text\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise ValueError(f"missing text block for heading: {heading}")
    return match.group(1).strip()


def extract_markdown_section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise ValueError(f"missing markdown section for heading: {heading}")
    return f"## {heading}\n\n{match.group(1).strip()}"


def read_source(args: argparse.Namespace) -> str:
    if args.source_file:
        return Path(args.source_file).read_text(encoding="utf-8").strip()
    if args.source:
        return args.source.strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def build_prompt(diagram_type: str, source: str, title: str | None) -> str:
    normalized_type = diagram_type.strip().lower()
    section = SECTION_BY_TYPE.get(normalized_type)
    if not section:
        allowed = ", ".join(sorted(SECTION_BY_TYPE))
        raise ValueError(f"unsupported diagram type '{diagram_type}'. Allowed: {allowed}")

    library = PROMPT_LIBRARY.read_text(encoding="utf-8")
    universal = extract_text_block(library, "Universal SVG Generation Prompt")
    specific = extract_text_block(library, section)
    review = extract_text_block(library, "Final Visual Review Prompt")
    archetypes = LAYOUT_ARCHETYPES.read_text(encoding="utf-8").strip()
    recipes_source = LAYOUT_RECIPES.read_text(encoding="utf-8")
    recipe_heading = RECIPE_BY_SECTION.get(section)
    recipe_sections = [extract_markdown_section(recipes_source, item) for item in COMMON_RECIPE_HEADINGS]
    if recipe_heading:
        recipe_sections.append(extract_markdown_section(recipes_source, recipe_heading))
    recipes = "\n\n".join(recipe_sections)

    title_text = title.strip() if title else "Untitled diagram"
    source_text = source.strip() if source else "[No source material provided. Ask the user for details before generating SVG.]"

    return "\n\n".join(
        [
            universal,
            specific,
            "Layout archetypes and placement discipline:\n" + archetypes,
            "Layout recipes and numeric design constraints:\n" + recipes,
            review,
            f"Diagram title:\n{title_text}",
            "User source material:\n" + source_text,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a high-quality SVG diagram prompt.")
    parser.add_argument("diagram_type", nargs="?", help="diagram type, e.g. architecture, swimlane, timeline")
    parser.add_argument("--source", help="source material inline")
    parser.add_argument("--source-file", help="path to source material")
    parser.add_argument("--title", help="diagram title")
    parser.add_argument("--list", action="store_true", help="list supported diagram types")
    args = parser.parse_args()

    if args.list:
        for item in sorted(SECTION_BY_TYPE):
            print(item)
        return 0

    if not args.diagram_type:
        parser.error("diagram_type is required unless --list is used")

    try:
        print(build_prompt(args.diagram_type, read_source(args), args.title))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
