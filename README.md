# lark-whiteboard-skill

A Codex skill for generating clean SVG diagrams from user input, validating the SVG, and handing it off to a Lark or Feishu whiteboard integration.

## Install

Clone this repository into another Codex CLI's skills directory:

```bash
git clone https://github.com/TobinZuo/lark-whiteboard-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/lark-whiteboard-skill"
```

Restart Codex or reload skills so `lark-whiteboard-skill` is discoverable.

Prerequisites for publishing into Lark:

- `lark-cli` installed and authenticated with document/whiteboard permissions.
- Node.js and `npx` available so the skill can run `@larksuite/whiteboard-cli`.

If you only want SVG generation, `lark-cli` is not required.

## What it does

- Turns common engineering diagrams into SVG: architecture, component, deployment topology, sequence, flowchart, swimlane, state machine, data flow, ERD, and CI/CD pipeline.
- Selects a diagram-specific prompt from `references/prompt-library.md` so the layout is intentionally designed instead of generic.
- Converts vague requests into a structured diagram brief before asking for SVG, inspired by observable MindAI-style task flows.
- Validates generated SVG with `scripts/validate_svg.py`.
- Hands the validated SVG to an available Lark or Feishu whiteboard skill or tool.
- Redacts whiteboard tokens from publish output by default.

This repository does not include Feishu authentication or board-writing API code. Those responsibilities are delegated to your existing whiteboard integration.

## Quick check

```bash
python3 scripts/validate_svg.py examples/simple-flow.svg
```

Build a diagram-specific prompt:

```bash
python3 scripts/build_prompt.py architecture --source "Client calls API, API calls worker, worker writes database." --title "Example Architecture"
```

Publish a validated SVG into a new Lark document whiteboard:

```bash
python3 scripts/publish_svg_to_lark_doc.py --svg diagram.svg --title "Example Architecture"
```

Preview the publish plan without writing to Lark:

```bash
python3 scripts/publish_svg_to_lark_doc.py --svg diagram.svg --title "Example Architecture" --dry-run
```

For agent integration, see `references/agent-contract.md`.
For the MindAI-style observations behind the current workflow, see `references/mindai-observable-patterns.md`.

## Examples

- `examples/system-architecture.svg`
- `examples/api-sequence.svg`
- `examples/er-diagram.svg`
- `examples/simple-flow.svg`

Validate all examples:

```bash
for f in examples/*.svg; do python3 scripts/validate_svg.py "$f"; done
```
