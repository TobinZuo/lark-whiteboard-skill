#!/usr/bin/env python3
"""Publish a validated SVG diagram into a Lark document whiteboard block."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise RuntimeError(f"command failed: {' '.join(cmd)}")
    return proc


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"missing required command: {name}")
    return path


def preflight(svg_path: Path, needs_lark: bool) -> dict[str, object]:
    checks: dict[str, object] = {
        "svg_exists": svg_path.exists(),
        "svg_path": str(svg_path),
        "npx": require_command("npx"),
    }
    if needs_lark:
        checks["lark_cli"] = require_command("lark-cli")
    if not svg_path.exists():
        raise RuntimeError(f"missing svg: {svg_path}")
    return checks


def load_json_output(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    if start == -1:
        raise ValueError("no JSON object found in command output")
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(text[start:])
    if not isinstance(obj, dict):
        raise ValueError("command output JSON is not an object")
    return obj


def parse_whiteboard_token(content: str) -> str:
    match = re.search(r'<whiteboard[^>]*token="([^"]+)"', content)
    if not match:
        raise ValueError("whiteboard token not found in fetched document content")
    return match.group(1)


def create_doc(title: str, markdown_path: Path) -> tuple[str, str]:
    proc = run(
        [
            "lark-cli",
            "docs",
            "+create",
            "--api-version",
            "v2",
            "--title",
            title,
            "--doc-format",
            "markdown",
            "--content",
            f"@{markdown_path}",
        ]
    )
    payload = load_json_output(proc.stdout)
    if not payload.get("ok"):
        raise RuntimeError(payload)
    document = payload["data"]["document"]
    doc_url = document["url"]
    whiteboard_token = document["new_blocks"][0]["block_token"]
    return doc_url, whiteboard_token


def fetch_doc(doc_url: str) -> tuple[str, str]:
    proc = run(["lark-cli", "docs", "+fetch", "--api-version", "v2", "--doc", doc_url])
    payload = load_json_output(proc.stdout)
    if not payload.get("ok"):
        raise RuntimeError(payload)
    document = payload["data"]["document"]
    return document["content"], document["document_id"]


def convert_svg(svg_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    openapi_path = out_dir / "board.openapi.json"
    run(
        [
            "npx",
            "-y",
            "@larksuite/whiteboard-cli@^0.2.0",
            "-i",
            str(svg_path),
            "-f",
            "svg",
            "--check",
        ]
    )
    proc = run(
        [
            "npx",
            "-y",
            "@larksuite/whiteboard-cli@^0.2.0",
            "-i",
            str(svg_path),
            "-f",
            "svg",
            "--to",
            "openapi",
            "--format",
            "json",
        ]
    )
    openapi_path.write_text(proc.stdout)
    return openapi_path


def update_whiteboard(token: str, openapi_path: Path, idempotent_token: str) -> None:
    run(
        [
            "lark-cli",
            "docs",
            "+whiteboard-update",
            "--whiteboard-token",
            token,
            "--input_format",
            "raw",
            "--source",
            f"@{openapi_path}",
            "--overwrite",
            "--idempotent-token",
            idempotent_token,
        ]
    )


def masked_token(token: str) -> str:
    if len(token) <= 8:
        return "<redacted>"
    return f"{token[:4]}...{token[-4:]}"


def export_preview(token: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = run(
        [
            "lark-cli",
            "whiteboard",
            "+query",
            "--whiteboard-token",
            token,
            "--output_as",
            "image",
            "--output",
            str(out_dir),
            "--overwrite",
        ]
    )
    payload = load_json_output(proc.stdout)
    if not payload.get("ok"):
        raise RuntimeError(payload)
    return Path(payload["data"]["preview_image_path"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a validated SVG diagram into Lark.")
    parser.add_argument("--svg", required=True, type=Path, help="validated SVG file")
    parser.add_argument("--title", required=True, help="document title")
    parser.add_argument("--doc-url", help="existing Lark doc URL to update")
    parser.add_argument("--output-dir", type=Path, default=Path("data/publish"))
    parser.add_argument("--dry-run", action="store_true", help="validate only, do not write to Lark")
    parser.add_argument("--idempotent-token", help="custom idempotent token")
    parser.add_argument("--include-token", action="store_true", help="include the real whiteboard token in JSON output")
    args = parser.parse_args()

    try:
        checks = preflight(args.svg, needs_lark=not args.dry_run)
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "stage": "preflight", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        markdown_path = tmp_path / "doc.md"
        markdown_path.write_text(
            "\n".join(
                [
                    f"# {args.title}",
                    "",
                    "<whiteboard type=\"blank\"></whiteboard>",
                    "",
                    "## 架构摘要",
                    "",
                    "- 本白板由 SVG 转换并写入。",
                ]
            )
        )

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "dry_run": True,
                        "stage": "preflight",
                        "checks": checks,
                        "planned_mode": "update_doc" if args.doc_url else "create_doc",
                        "title": args.title,
                        "doc_url": args.doc_url,
                    },
                    ensure_ascii=False,
                )
            )
            return 0

        if args.doc_url:
            content, doc_id = fetch_doc(args.doc_url)
            token = parse_whiteboard_token(content)
            doc_url = args.doc_url
        else:
            doc_url, token = create_doc(args.title, markdown_path)
            doc_id = doc_url.rsplit("/", 1)[-1]

        openapi_path = convert_svg(args.svg, args.output_dir)
        idempotent = args.idempotent_token or f"{doc_id.replace('/', '')}-svg-publish"
        update_whiteboard(token, openapi_path, idempotent)
        preview_path = export_preview(token, args.output_dir / "export")

        print(
            json.dumps(
                {
                    "ok": True,
                    "doc_url": doc_url,
                    "document_id": doc_id,
                    "whiteboard_token": token if args.include_token else masked_token(token),
                    "whiteboard_token_redacted": not args.include_token,
                    "openapi_path": str(openapi_path),
                    "preview_path": str(preview_path),
                },
                ensure_ascii=False,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
