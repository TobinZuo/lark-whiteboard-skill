# lark-whiteboard-skill

Create clear architecture diagrams, flowcharts, sequence diagrams, data flows, and other structured visuals for Lark or Feishu whiteboards.

This skill helps you turn rough descriptions into diagrams that are ready to review, share, or publish into a document. It is useful when a conversation, design note, incident summary, or system description needs to become a visual artifact quickly.

## What You Can Ask For

- "Draw the architecture of our search engine."
- "Turn this release process into a flowchart."
- "Create a sequence diagram for login and token refresh."
- "Make a data flow diagram from ingestion to warehouse to dashboard."
- "Convert this schema description into an ER diagram."
- "Generate a diagram I can put into a Feishu whiteboard."

## What It Helps With

- Clarifies messy system descriptions into a readable visual.
- Chooses a diagram type that fits the request instead of making a generic box-and-arrow drawing.
- Keeps labels, spacing, and arrows clean enough for whiteboard review.
- Produces portable SVG files that can be reused outside Lark or Feishu.
- Can publish a finished SVG into a Lark document whiteboard when your local Lark tools are configured.

Supported diagram types include architecture, component, deployment topology, sequence, flowchart, process, swimlane, state machine, data flow, ERD, CI/CD pipeline, org chart, timeline, mind map, matrix, and funnel.

## Install

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/TobinZuo/lark-whiteboard-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/lark-whiteboard-skill"
```

Restart Codex or reload skills so `lark-whiteboard-skill` is discoverable.

## Publishing To Lark Or Feishu

SVG generation works without Lark setup.

To publish into a Lark document whiteboard, install and authenticate the Lark tooling used in your environment:

- `lark-cli` with document and whiteboard permissions.
- Node.js and `npx` so the whiteboard converter can run.

If publishing is not configured, the skill still returns the SVG path so you can import or share it manually.

## Developer Checks

Validate an example SVG:

```bash
python3 scripts/validate_svg.py examples/simple-flow.svg
```

Preview a publish plan without writing to Lark:

```bash
python3 scripts/publish_svg_to_lark_doc.py --svg examples/system-architecture.svg --title "System Architecture" --dry-run
```

For agent integration details, see `references/agent-contract.md`.
