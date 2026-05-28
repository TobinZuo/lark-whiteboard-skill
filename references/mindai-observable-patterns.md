# MindAI Observable Patterns

This note captures observable product and workflow patterns from MindAI-style chart generation. It does not describe or infer private server-side implementation.

## What The Tool Appears To Do Well

- It treats a diagram request as a task with lifecycle events, not as a one-shot text answer.
- It separates the first useful artifact, an SVG, from later publishing steps such as creating or updating a Lark document.
- It keeps task state resumable with a task id, latest SVG path, event cursor, chat URL, and optional document URL.
- It normalizes streaming progress into compact events that other agents can parse.
- It gathers authentication and document-writing concerns inside deterministic client code instead of asking the model to improvise API calls.
- It lets the model focus on content planning and diagram generation while scripts own validation, conversion, upload, and final status reporting.

## Observed SVG Shape, Not A Template

A cached MindAI whiteboard SVG on this machine had these concrete traits. Treat them as evidence of priorities, not as a template to copy:

- Canvas: `1200 x 820`, no oversized title, and a small generated-by watermark.
- Elements: 116 total elements, including 49 editable `text` nodes, 19 `rect` nodes, 25 `path` nodes, and 14 small `circle` markers.
- Zones: four large light-gray rounded background containers for functional areas.
- Legend: compact top-right legend distinguishing solid synchronous request links from dashed asynchronous event links.
- Nodes: compact rounded rectangles, usually 160-240 px wide and 50-100 px tall, with a small colored dot on the left.
- Typography: mostly 12-16 px text, using bold 14-16 px node titles and 10-12 px edge labels.
- Palette: muted Feishu-like colors: blue for sync request flow, red/orange for async event flow, green for data/compute, amber for core decisioning, and neutral gray for containers.
- Connectors: simple orthogonal `path` routes with thin 1.5 px strokes; dashed paths encode async/event movement.
- Information design: the main online path sits in the upper zones, while data and computation form a bottom foundation lane.

The useful reverse-engineered signal is not the exact size, palette, or positions. The useful signal is that the generator appears to choose an information architecture first, then uses a restrained SVG vocabulary to make the chosen relationships easy to scan.

## Generation Implications For This Skill

Use a structured diagram brief before drawing:

- Goal: what the viewer should understand.
- Scope boundary: what systems or phases are included and excluded.
- Entities: actors, services, data stores, states, teams, or milestones.
- Relationships: calls, data movement, ordering, ownership, control, retry, or failure paths.
- Main story: the dominant reading path that should be visible first.
- Secondary context: annotations that help but must not crowd the layout.

For architecture diagrams with online and offline flows, consider a compact whiteboard composition when it clarifies the source:

- Use zones only when they express real boundaries in the source.
- Separate primary, secondary, and operational paths without forcing a specific layout.
- Include a legend only when line styles or colors encode meaning.
- Use orthogonal arrows and concise edge labels where they improve scanability.
- Distinguish sync request paths from async event/message paths when the source has both.

Treat SVG readiness as the first success milestone:

- Produce a self-contained SVG.
- Validate it locally.
- Return the SVG path and validation result even when publishing is not requested.
- Publish only when a target document or explicit create request exists.

Keep handoff output machine-readable:

- Scripts should print JSON for automation-friendly operations.
- Sensitive tokens should be redacted by default.
- Failure messages should include the stage that failed.

## Quality Heuristics To Emulate

- Prefer a balanced, readable diagram over exhaustive coverage.
- Use stable zones or lanes when a request has multiple flows.
- Put the primary path in a strong visual direction, usually left-to-right for architecture and data flow.
- Route secondary or operational feedback paths with lighter strokes.
- Avoid placing storage, queues, and observability as floating decoration; attach them to the services or stages that own them.
- Keep labels short and manually wrapped, because whiteboard import can change font metrics.

## Boundaries

Do not copy remote APIs, event contracts, or private implementation details into this skill unless they are public and intentionally part of a supported integration. This repository should remain a local SVG generation and Lark handoff skill.
