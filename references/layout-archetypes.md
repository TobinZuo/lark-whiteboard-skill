# Layout Archetypes

Use one layout archetype per diagram unless the user explicitly asks for a hybrid.

## Pick One

- `left-right pipeline`: request/response paths, service chains, layered architectures.
- `top-down stack`: control planes, infrastructure layers, dependency ladders.
- `split-band`: online plus offline paths, or core path plus ops/observability.
- `swimlane`: responsibility changes across actors or systems.
- `hub-and-spoke`: one central coordinator fans out to satellites.
- `ring or loop`: feedback loops, monitoring, continuous cycles.

## Non-Negotiable Rules

- Choose the archetype before placing any node.
- Use one dominant reading direction.
- Keep same-level nodes on one row or one column.
- Put stores, queues, and indexes close to the services that own or read them.
- Put external systems at the edge of the canvas.
- Keep monitoring, analytics, and ops feedback loops in a separate side band.
- If the graph is dense, split it into bands instead of shrinking everything.

## Good Defaults

- Online request paths: `left-right pipeline`
- Multi-phase platforms: `top-down stack`
- Batch plus realtime: `split-band`
- Cross-team workflows: `swimlane`
- Control center plus satellites: `hub-and-spoke`

## Anti-Patterns

- Freeform clouds of boxes.
- Multiple competing reading directions.
- Floating storage nodes.
- Diagonal connectors as the default.
- Interleaving online and offline modules in the same row.
- Using different node sizes for peers without semantic reason.
