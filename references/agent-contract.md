# Agent Contract

This skill is reusable when other agents treat it as a three-stage interface:

1. Input a diagram request.
2. Produce a validated SVG.
3. Publish the SVG into a Lark document whiteboard.

## Input Contract

Required:

- `title`
- `diagram_type`
- `source` or `source_file`

Optional:

- `doc_url`
- `target_mode` (`create_doc` or `update_doc`)
- `publish` (`true` or `false`)
- `explain_only` (`true` or `false`)

## Output Contract

The skill should return:

- `svg_path`
- `validation_result`
- `source_summary`
- `publish_stage` when publishing is attempted
- `doc_url` when published
- `whiteboard_token` only when explicitly requested; otherwise return a redacted token
- `preview_path` when published

## Reuse Rule

Other agents should not hardcode Lark API calls. They should call:

```bash
python3 scripts/build_prompt.py <diagram_type> --source-file <source.txt> --title "<title>"
python3 scripts/validate_svg.py <diagram.svg>
python3 scripts/publish_svg_to_lark_doc.py --svg <diagram.svg> --title "<title>"
```

This keeps the generation step model-driven and the publish step deterministic.

Use `publish_svg_to_lark_doc.py --dry-run` before a real publish when an agent needs to verify local dependencies or explain the planned write target.

## Installation For Another Codex CLI

```bash
git clone https://github.com/TobinZuo/lark-whiteboard-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/lark-whiteboard-skill"
```

Then restart Codex or reload skills. To smoke test:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/lark-whiteboard-skill/scripts/validate_svg.py" \
  "${CODEX_HOME:-$HOME/.codex}/skills/lark-whiteboard-skill/examples/system-architecture.svg"
```
