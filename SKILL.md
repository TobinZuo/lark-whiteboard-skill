---
name: lark-whiteboard-skill
description: Generate clean SVG diagrams from user descriptions and hand them off to a Lark or Feishu whiteboard creation skill or tool. Use when the user asks to create, draw, convert, or sync architecture diagrams, flowcharts, process maps, mind maps, org charts, timelines, or other structured visuals into a Lark or Feishu whiteboard, especially when the workflow should start from model-generated SVG.
---

# Lark Whiteboard Skill

## Overview

Use this skill to turn a user's diagram request into a portable SVG artifact, validate that artifact, then pass it to an available Lark or Feishu whiteboard skill or tool to create the final whiteboard.

This skill owns the SVG generation workflow. It does not own Feishu authentication, board creation APIs, or document mutation; delegate those steps to the environment's Lark or Feishu whiteboard integration.

## Workflow

1. Clarify only missing delivery-critical inputs:
   - Target Lark or Feishu whiteboard or document URL, if the user expects direct publishing.
   - Diagram type, audience, and source material, if the request is ambiguous.
   - Whether text should remain editable on the board, if the downstream tool supports both editable objects and flat image import.
2. Convert the user's input into a concise diagram plan:
   - Identify entities, relationships, direction, swimlanes, groups, sequence, and key labels.
   - Preserve user-provided names exactly.
   - Do not invent business facts, systems, owners, metrics, or dependencies.
   - Write down the intended story in one sentence, then list the minimum nodes and edges needed to tell it.
   - Separate online/request flow, offline/data flow, control flow, and operational feedback when they would otherwise crowd one diagram.
3. Select the best diagram prompt:
   - Classify the request using [references/prompt-library.md](references/prompt-library.md).
   - Combine the universal SVG prompt, the relevant diagram-type prompt, and the final visual review prompt.
   - Choose a layout archetype from [references/layout-archetypes.md](references/layout-archetypes.md) before rendering; do not place nodes before the dominant direction is fixed.
   - Prefer `python3 scripts/build_prompt.py <diagram-type> --source-file source.txt --title "Title"` when source material is in a file or long enough that manual prompt assembly is error-prone.
   - If the request fits multiple diagram types, choose the type that makes the relationships easiest to scan.
4. Generate an SVG file:
   - Prefer simple vector primitives: `rect`, `circle`, `ellipse`, `line`, `polyline`, `path`, `text`, and `g`.
   - Use deterministic layout with a clear `viewBox`, explicit dimensions, and readable text.
   - Follow [references/svg-guidelines.md](references/svg-guidelines.md).
   - Follow [references/layout-recipes.md](references/layout-recipes.md) for canvas size, node dimensions, spacing, typography, and palettes.
5. Validate the SVG:
   - Run `python3 scripts/validate_svg.py path/to/diagram.svg`.
   - Inspect the SVG for visual quality before handoff; regenerate once if the layout is crowded, unbalanced, or unclear.
   - Fix validation errors before handoff.
   - Prefer rerunning validation with `--json` when another agent or automation needs a stable result object.
6. Hand off to the Lark or Feishu whiteboard integration:
   - Follow [references/whiteboard-handoff.md](references/whiteboard-handoff.md).
   - For a reusable agent flow, follow [references/agent-contract.md](references/agent-contract.md).
   - If no target URL was provided, return the SVG path and ask where to publish it.
   - If no whiteboard integration is available, return the SVG path and state that publishing could not be completed in the current environment.

## Reusable Agent Interface

Expose this skill to other agents as a split workflow:

1. Prompt construction:
   ```bash
   python3 scripts/build_prompt.py architecture --source-file request.txt --title "System Architecture"
   ```
2. SVG validation:
   ```bash
   python3 scripts/validate_svg.py diagram.svg
   ```
3. Lark document publishing:
   ```bash
   python3 scripts/publish_svg_to_lark_doc.py --svg diagram.svg --title "System Architecture"
   ```

Keep the model-driven part limited to SVG generation. Keep Lark document creation, SVG conversion, whiteboard update, and preview export in `scripts/publish_svg_to_lark_doc.py`.

## Generation Workflow Principles

This skill intentionally stays local, transparent, and portable. Keep the generation workflow explicit:

- Turn vague requests into a structured diagram brief before drawing.
- Keep the generation artifact resumable: source request, prompt, SVG path, validation result, and publish result should be easy to pass between agents.
- Treat SVG readiness as the first success milestone; publishing to Lark or Feishu is a separate step.
- Return stable JSON from scripts when automation is involved.
- Avoid exposing sensitive whiteboard tokens in user-facing output unless a downstream tool explicitly requires them.
- Prefer explicit progress and failure messages over silent best-effort publishing.

## Prompt Selection

Always use [references/prompt-library.md](references/prompt-library.md) before generating SVG. Do not use a generic "make a diagram" prompt when a diagram-specific prompt applies.

For repeatable prompt construction, run:

```bash
python3 scripts/build_prompt.py architecture --source-file request.txt --title "System Architecture"
```

Prioritize common engineering diagrams:

- System or service architecture: `architecture`.
- Module/package boundaries and internal responsibilities: `component`.
- Machines, VPCs, Kubernetes, regions, clusters, gateways: `deployment`.
- API calls, RPC, events, request/response chains: `sequence`.
- Business or engineering workflow, release flow, approval flow: `flowchart` or `process`.
- Cross-team or cross-system responsibility over time: `swimlane`.
- State transitions, lifecycle, retry/failure states: `state-machine`.
- Data movement, ETL, stream/batch pipeline, lineage: `data-flow`.
- Tables, fields, entities, relationships: `erd`.
- Build, test, release, deploy automation: `ci-cd`.

Use generic business prompts such as org chart, timeline, mind map, matrix, or funnel only when the user clearly asks for them.

## SVG Quality Bar

Produce diagrams that are useful after import into a whiteboard:

- Keep the SVG self-contained. Do not reference external fonts, images, CSS, scripts, or network resources.
- Prefer editable text elements over outlined text.
- Use a restrained palette with strong contrast and no single-color theme.
- Keep labels short enough to fit inside their shapes; wrap manually with `tspan`.
- Use arrowheads, grouping, spacing, and visual hierarchy to make relationships obvious.
- Put the title inside the SVG only when it helps the board artifact stand alone.
- Avoid decorative backgrounds, gradients, shadows, and dense illustration.
- Leave generous margins and whitespace. A smaller, clearer diagram is better than a crowded one.
- Use a clear type scale: title 40-52 px, group labels 24-32 px, node labels 20-28 px, supporting labels 16-20 px.

## Diagram Defaults

Use these defaults unless the user or source material indicates otherwise:

- Architecture diagrams: one dominant reading direction, usually left-right or split-band; do not interleave online and offline paths in one row.
- Component diagrams: layered layout from interface/adapters to domain/core to infrastructure.
- Deployment diagrams: outer-to-inner grouping from region/VPC/cluster/namespace to workloads and backing services.
- Process diagrams: top-to-bottom or left-to-right numbered stages, with branches only where decisions are explicit.
- Swimlanes: lanes represent actors, teams, systems, or lifecycle phases named by the user.
- State machines: one node per state, one labeled directed edge per explicit transition.
- Data flow diagrams: left-to-right from producers through processing stages to sinks/consumers.
- ER diagrams: entities as table cards, fields as rows, relationships as labeled connectors.
- Timelines: horizontal axis with evenly spaced dated or ordered milestones.
- Org charts: top-down hierarchy, with dotted edges only for advisory or non-reporting relationships explicitly stated by the user.

## Handoff Rule

After validation succeeds, treat the SVG as the source of truth. Do not manually rebuild a second, divergent diagram for the whiteboard unless the downstream tool cannot consume SVG and requires an explicit element-by-element conversion.
