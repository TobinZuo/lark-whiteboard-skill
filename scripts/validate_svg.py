#!/usr/bin/env python3
"""Validate SVG files before sending them to a whiteboard importer."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


FORBIDDEN_TAGS = {
    "script",
    "foreignObject",
    "iframe",
    "object",
    "embed",
    "audio",
    "video",
    "canvas",
}
WARN_TAGS = {"image", "style"}
URL_PATTERN = re.compile(r"url\s*\(([^)]*)\)", re.IGNORECASE)
CSS_FORBIDDEN_PATTERN = re.compile(r"(@import|expression\s*\(|javascript:)", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_number(value: str | None, field: str) -> float:
    if value is None or not value.strip():
        raise ValueError(f"missing {field}")
    match = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*(?:px)?\s*", value)
    if not match:
        raise ValueError(f"{field} must be a positive numeric value")
    number = float(match.group(1))
    if number <= 0:
        raise ValueError(f"{field} must be positive")
    return number


def parse_viewbox(value: str | None) -> list[float]:
    if value is None or not value.strip():
        raise ValueError("missing viewBox")
    parts = re.split(r"[\s,]+", value.strip())
    if len(parts) != 4:
        raise ValueError("viewBox must contain four numbers")
    numbers = [float(part) for part in parts]
    if numbers[2] <= 0 or numbers[3] <= 0:
        raise ValueError("viewBox width and height must be positive")
    return numbers


def has_external_url(value: str) -> bool:
    for match in URL_PATTERN.finditer(value):
        target = match.group(1).strip().strip("\"'")
        if not target.startswith("#"):
            return True
    return False


def inspect_svg(path: Path, max_bytes: int, max_elements: int) -> dict[str, object]:
    data = path.read_bytes()
    errors: list[str] = []
    warnings: list[str] = []

    if len(data) > max_bytes:
        errors.append(f"file exceeds max size: {len(data)} > {max_bytes} bytes")

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        return {
            "ok": False,
            "errors": [f"invalid XML: {exc}"],
            "warnings": warnings,
            "elements": 0,
        }

    if local_name(root.tag) != "svg":
        errors.append("root element must be <svg>")

    try:
        width = parse_number(root.attrib.get("width"), "width")
        height = parse_number(root.attrib.get("height"), "height")
    except ValueError as exc:
        errors.append(str(exc))
        width = None
        height = None

    try:
        viewbox = parse_viewbox(root.attrib.get("viewBox"))
    except ValueError as exc:
        errors.append(str(exc))
        viewbox = None

    element_count = 0
    text_count = 0
    for elem in root.iter():
        element_count += 1
        tag = local_name(elem.tag)

        if tag in FORBIDDEN_TAGS:
            errors.append(f"forbidden element <{tag}>")
        if tag in WARN_TAGS:
            warnings.append(f"avoid <{tag}> unless the downstream importer supports it")
        if tag == "text":
            text_count += 1

        if elem.text and CSS_FORBIDDEN_PATTERN.search(elem.text):
            errors.append(f"forbidden CSS or script-like content inside <{tag}>")

        for attr_name, attr_value in elem.attrib.items():
            attr_local = local_name(attr_name)
            value = attr_value.strip()
            if attr_local.lower().startswith("on"):
                errors.append(f"event handler attribute is not allowed: {attr_local}")
            if attr_local in {"href", "src"} and value and not value.startswith("#"):
                errors.append(f"external reference is not allowed: {attr_local}={value}")
            if "style" in attr_local.lower() and CSS_FORBIDDEN_PATTERN.search(value):
                errors.append(f"forbidden CSS content in {attr_local}")
            if has_external_url(value):
                errors.append(f"external url() references are not allowed in {attr_local}")

    if element_count > max_elements:
        errors.append(f"too many elements: {element_count} > {max_elements}")

    if text_count == 0:
        warnings.append("no <text> elements found; labels may not be editable after import")

    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "elements": element_count,
        "text_elements": text_count,
        "width": width,
        "height": height,
        "viewBox": viewbox,
        "bytes": len(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SVG for Lark or Feishu whiteboard handoff.")
    parser.add_argument("svg_path", type=Path)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--max-elements", type=int, default=2_000)
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    if not args.svg_path.exists():
        print(f"ERROR: file not found: {args.svg_path}", file=sys.stderr)
        return 2

    result = inspect_svg(args.svg_path, args.max_bytes, args.max_elements)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "OK" if result["ok"] else "ERROR"
        print(f"{status}: {args.svg_path} ({result.get('elements', 0)} elements)")
        for error in result["errors"]:
            print(f"error: {error}")
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
