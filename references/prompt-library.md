# Prompt Library

Use this library to generate attractive, clear SVG diagrams. Compose prompts in this order:

1. Universal SVG generation prompt.
2. One diagram-specific prompt.
3. Final visual review prompt.

Ask the model for the SVG only. Do not ask for Markdown, explanations, or comments around the SVG.

## Universal SVG Generation Prompt

```text
You are an expert information designer creating a polished SVG diagram for a Lark/Feishu whiteboard.

Task:
Create one self-contained SVG from the user's source material.

Hard requirements:
- Output only valid SVG markup, starting with <svg and ending with </svg>.
- Use width, height, and viewBox on the root SVG.
- Use editable <text> labels with font-family="Arial, Helvetica, sans-serif".
- Use only inline SVG primitives: rect, circle, ellipse, line, polyline, polygon, path, text, tspan, g, defs, marker, title, desc.
- Do not use script, foreignObject, external images, external CSS, @import, url() to external resources, emoji, or icon fonts.
- Preserve all user-provided names exactly.
- Do not invent systems, teams, metrics, owners, or dependencies not present in the source.

Visual quality requirements:
- Make the diagram clean, balanced, and professional enough for an executive or engineering review.
- Use a structured layout grid with consistent alignment.
- Use generous whitespace and avoid crowding.
- Keep arrows short and route them around labels.
- Use no more than 5 semantic colors, with high contrast and a neutral background.
- Use visual hierarchy: large title, clear section labels, readable node labels, lighter secondary annotations.
- Wrap long labels manually using <tspan>; never let text overflow its container.
- Prefer fewer, well-spaced elements over a dense diagram.
- Before drawing, choose one layout archetype and use it for the whole diagram.
- Reserve semantic bands or columns first, then place nodes inside those bands.
- Do not mix left-right and top-down flows on the same visual spine.
```

## Architecture Prompt

Use for service maps, platform diagrams, system dependencies, data flow, and infra diagrams.

```text
Diagram type: architecture.

Layout:
- Use one dominant layout archetype. For most architecture diagrams, prefer `left-right pipeline` or `split-band`.
- Reserve explicit bands before placing nodes: entry, edge/API, services, data/storage, external/ops.
- Use a left-to-right flow for the core path unless the source clearly suggests a different dominant direction.
- Group related components into lightly stroked zones only when grouping is explicit or strongly implied.
- Place databases and queues near the services that own or use them.
- Use solid arrows for request/data flow and dashed arrows only for optional, async, or control paths that are explicit in the source.
- Keep every node on a grid; avoid diagonal spaghetti lines.
- If the source contains both online and offline logic, separate them into bands or rows instead of interleaving them.
- Keep monitoring, alerting, analytics, and ops feedback loops in a separate side band.

Styling:
- Use rounded rectangles for services, cylinders or database-shaped groups for storage, small pills for external systems.
- Give each zone a subtle tint but keep node fills mostly light.
- Use one accent color for the primary path and neutral strokes for secondary relationships.
```

## Component Prompt

Use for codebase/module structure, package boundaries, layered architecture, plugin systems, SDKs, and ownership boundaries inside one system.

```text
Diagram type: component.

Layout:
- Use a layered layout: entrypoints/interfaces at the top or left, application/domain modules in the center, infrastructure/adapters at the bottom or right.
- Group components by package, bounded context, repo, or runtime boundary only when that grouping appears in the source.
- Show dependencies with directed arrows from caller/importer to callee/imported module.
- Keep cycles visible if they exist; do not hide or "fix" cyclic dependencies.
- Use one node per component, package, module, or responsibility named in the source.
- Make boundaries legible: distinguish public API, orchestration/application logic, domain/core logic, adapters, and infrastructure when the source supports it.
- Put shared utilities, cross-cutting concerns, and external integrations at the edge so they do not obscure the main dependency path.
- Show ownership or runtime boundaries only when they clarify deployability, package structure, or responsibility.

Styling:
- Use simple rounded rectangles for components.
- Use subtle group boundaries for packages or layers.
- Use thicker or colored arrows for primary dependency paths and neutral arrows for secondary imports.
- Keep implementation details as small secondary labels inside the component only when important.
- Avoid class-diagram detail unless the user asks for code-level internals.
```

## Deployment Topology Prompt

Use for infrastructure, Kubernetes, cloud regions, networks, clusters, hosts, runtimes, gateways, and production/staging deployment views.

```text
Diagram type: deployment topology.

Layout:
- Use nested boundaries from largest to smallest: region, VPC/network, cluster, namespace/subnet, workload/pod/service.
- Put ingress, gateway, load balancer, or public entry points on the left/top edge of the topology.
- Put internal services in the center and backing services such as databases, queues, object storage, and caches to the right/bottom.
- Show network or request paths with directed arrows.
- Keep security, network, or runtime boundaries visually obvious.
- Separate environments such as prod, staging, standby, or DR only when they appear in the source.
- Show trust boundaries, private/public zones, and managed services as boundaries rather than standalone decorations.
- Put scaling units such as replicas, pods, nodes, or autoscaling groups inside the scope that owns them.

Styling:
- Use large light boundary boxes for infrastructure scopes.
- Use compact workload cards for services, jobs, pods, containers, and hosts.
- Use storage-specific shapes or clearly labeled storage cards.
- Use dashed lines only for optional, failover, or management paths explicitly stated by the source.
- Avoid cloud-provider icon clutter; use labeled primitives unless a specific icon set is provided.
```

## Data Flow Prompt

Use for ETL, streaming, batch jobs, event pipelines, lineage, ingestion, feature pipelines, data processing, and producer-to-consumer flows.

```text
Diagram type: data flow.

Layout:
- Use left-to-right flow: sources, ingestion, processing, storage, serving, consumers.
- Separate batch and streaming paths into parallel rows when both exist.
- Show the maturity of data as it moves through the system: raw, staged, curated, metric marts, semantic layer, and dashboard/consumer outputs when these stages fit the source.
- Put validation, schema checks, deduplication, enrichment, aggregation, and quality gates as first-class stages when the source implies operational trust.
- Show data stores near the stage that writes or owns them, and label whether they hold raw events, clean tables, marts, features, or published metrics.
- Use separate rows or bands for streaming, batch, and operational metadata/quality flows; do not mix them into one undifferentiated chain.
- Label arrows with data type, topic/table name, or cadence only if supplied by the source.
- Make lineage obvious: a viewer should be able to trace how one dashboard metric flows back to its upstream source.

Styling:
- Use distinct but restrained colors for source, ingestion, processing, storage, semantic/serving, consumers, and quality/control nodes.
- Use cylinder-like or storage-labeled nodes for databases, warehouses, lakes, queues, topics, and object stores.
- Use thick arrows for primary data movement and thin arrows for metadata/control flow.
- Use dashed arrows for quality alerts, catalog metadata, orchestration triggers, or monitoring feedback only when those paths are present.
- Avoid decorative dashboard mockups; represent dashboards as consumer artifacts with the metric or audience they serve.
```

## Flowchart Or Process Prompt

Use for procedures, approvals, decision trees, state transitions, and lifecycle steps.

```text
Diagram type: flowchart/process.

Layout:
- Use top-to-bottom for short operational procedures and left-to-right for product or lifecycle flows.
- Number major stages when order matters.
- Use diamonds only for explicit decisions.
- Put "yes/no" or branch labels close to the outgoing arrow, not inside the decision node.
- Keep main flow visually dominant; route exception paths to the side.
- Preserve roles, inputs, outputs, approvals, retries, and terminal outcomes when the source mentions them.
- Collapse repeated low-value steps into one stage rather than making a long checklist diagram.
- Put exception paths below or to the side and route them back to the recovery point or terminal failure.

Styling:
- Use consistent stage cards with compact labels.
- Use one accent color for the main path, one warning color for exceptions, and neutral colors for normal steps.
- Avoid more than two branches from a single decision unless the source explicitly requires it.
- Use stage numbers or phase labels when they help the viewer follow sequence quickly.
```

## CI/CD Pipeline Prompt

Use for build, test, package, release, deployment, rollback, environment promotion, and automation workflows.

```text
Diagram type: CI/CD pipeline.

Layout:
- Use left-to-right stages from code change to production outcome.
- Group stages by environment or responsibility: source, CI, artifact, staging, production, verification.
- Show gates such as approval, quality checks, canary, rollback, and monitoring only when present in the source.
- Put failure paths below the main pipeline and route them back to the relevant retry or rollback point.
- Show artifacts as first-class handoffs: package, image, manifest, release tag, or deployment bundle when present.
- Separate build/test/release/deploy/verify so the viewer can see where quality gates happen.
- Put rollback, hotfix, and incident-triggered paths below the happy path.

Styling:
- Use numbered stage cards or a connected pipeline rail.
- Use green or primary accent for the happy path, amber for manual gates, red only for failure/rollback.
- Use compact badges for artifacts, images, versions, or environments.
- Do not draw every individual test unless the user is asking for detailed CI internals.
```

## Swimlane Prompt

Use when responsibility across teams, actors, or systems matters.

```text
Diagram type: swimlane.

Layout:
- Use horizontal lanes for actors/teams/systems unless the source clearly suggests vertical lanes.
- Place lane labels in a fixed left column.
- Lay out steps chronologically from left to right.
- Keep each step inside the lane responsible for it.
- Use cross-lane arrows only when ownership changes or a handoff occurs.
- Make handoffs the visual focus: label what is handed off, not only who sends it.
- Keep each lane's steps aligned to the same time grid so parallel work is visible.
- Put approvals, escalations, and rework loops in the lane that owns the decision.

Styling:
- Use subtle alternating lane backgrounds.
- Keep lane headers compact and high contrast.
- Use consistent step boxes and avoid decorative grouping inside lanes.
- Avoid duplicating the same step in multiple lanes; use one owner and a labeled handoff.
```

## Sequence Prompt

Use for API calls, message exchange, request/response flows, and event chains.

```text
Diagram type: sequence.

Layout:
- Put participants as columns across the top.
- Use vertical lifelines and horizontal message arrows.
- Order messages from top to bottom.
- Use dashed return arrows only when returns are explicit and useful.
- Group optional or async segments with labeled brackets when present in the source.
- Separate synchronous calls, asynchronous events, callbacks, and retries using distinct line styles only when the source includes them.
- Keep participant count small; group internal services behind a single participant when details are not supplied.
- Show error or timeout paths as side segments rather than mixing them into the happy path.

Styling:
- Use compact participant headers.
- Keep message labels short and aligned above arrows.
- Leave enough vertical spacing between messages for readability.
- Avoid activation bars unless nested execution needs to be understood.
```

## State Machine Prompt

Use for lifecycle states, retry logic, job states, workflow status, order/payment status, protocol states, and failure recovery.

```text
Diagram type: state machine.

Layout:
- Use one rounded node per state.
- Use directed edges for transitions and label each edge with the event, condition, or action from the source.
- Place the initial state at the upper left or top center.
- Place terminal success states toward the right/bottom and failure/cancelled states below the main path.
- Keep retry loops compact and visibly connected to the state they retry.
- Separate stable states from transient actions; actions should usually be edge labels, not nodes.
- Group waiting, retry, failure, and manual intervention states when they form a recovery region.
- Do not add success, failure, or cancelled states unless the source implies them.

Styling:
- Use neutral fills for normal states, green for terminal success, amber for waiting/retry, and red for failed/cancelled states only when those meanings exist.
- Use curved arrows for self-loops or retry loops.
- Avoid unlabeled transitions unless the source explicitly uses an implicit transition.
- Keep transition labels shorter than state labels; split long conditions into multiple edges only when necessary.
```

## ER Diagram Prompt

Use for database schemas, entity relationships, table design, domain models, fields, primary keys, foreign keys, and cardinality.

```text
Diagram type: ER diagram.

Layout:
- Use one table card per entity.
- Put the entity/table name in a strong header.
- List fields as rows, with primary keys first, then foreign keys, then important attributes.
- Place related entities close together.
- Draw relationship connectors between foreign key rows or between table edges when row-level connectors would be too crowded.
- Add cardinality labels such as 1, N, 0..1, or 1..N only if supplied or directly implied by keys.
- Group tables by bounded context, schema, or domain only when the source gives that grouping.
- Show join tables, bridge entities, and lookup tables distinctly when they are present.
- Keep audit fields, timestamps, and low-signal attributes out unless they matter to the requested design.

Styling:
- Use compact table cards with clear row dividers.
- Use subtle header fills and high-contrast text.
- Use relationship lines that avoid crossing table bodies where possible.
- Do not invent field types, keys, indexes, or cardinality.
- Use compact PK/FK tags rather than verbose key descriptions.
```

## Org Chart Prompt

Use for reporting lines, ownership, team structure, or role hierarchy.

```text
Diagram type: org chart.

Layout:
- Use top-down hierarchy.
- Put the highest-level role or group at the top center.
- Use balanced spacing between sibling nodes.
- Use dotted connectors only for advisory, shared, or non-reporting relationships explicitly stated by the user.
- Distinguish reporting lines, ownership, advisory relationships, and shared responsibilities only when the source states them.
- Group teams under departments or functions when it reduces visual clutter.
- Keep matrix relationships to a minimum; show them as dotted lines with labels.

Styling:
- Use consistent person/team cards.
- Emphasize group or department names over minor metadata.
- Avoid photos, avatars, or decorative icons unless provided by the user.
- Keep names, roles, and team labels short enough to scan at whiteboard zoom.
```

## Timeline Prompt

Use for roadmaps, milestones, releases, phases, and dated sequences.

```text
Diagram type: timeline.

Layout:
- Use a horizontal timeline for fewer than 10 milestones; use stacked phase rows for denser roadmaps.
- Preserve exact dates, quarters, or phase names from the source.
- Place milestones above and below the axis alternately only when it improves readability.
- Show duration as bars and point events as markers.
- Separate committed, tentative, and dependency-driven milestones only when the source identifies uncertainty.
- Use lanes for workstreams, teams, or releases when a single axis would hide parallel work.
- Keep date spacing proportional only when exact dates are supplied; otherwise use evenly spaced phases.

Styling:
- Use strong labels for phases, lighter labels for details.
- Use muted colors for future or tentative items only when the source indicates uncertainty.
- Avoid inventing dates, owners, durations, or dependency links.
```

## Mind Map Prompt

Use for idea breakdowns, taxonomies, planning maps, and concept relationships.

```text
Diagram type: mind map.

Layout:
- Put the central concept in the middle.
- Arrange first-level branches evenly around the center.
- Keep second-level nodes close to their parent branch.
- Avoid crossing branch lines.
- Limit first-level branches to the strongest categories; merge or omit weak branches rather than filling every direction.
- Keep each branch visually self-contained so child nodes read as part of the parent idea.
- Use radial layout for exploration and tree layout for taxonomies when hierarchy matters more than brainstorming.

Styling:
- Use distinct colors for first-level branches and lighter tints for child nodes.
- Keep labels concise and readable.
- Use curved connectors sparingly; clarity is more important than ornament.
- Do not turn a process or dependency graph into a mind map if arrows and order matter.
```

## Matrix Prompt

Use for 2x2 comparisons, prioritization, segmentation, and tradeoff maps.

```text
Diagram type: matrix.

Layout:
- Use two labeled axes with clear low/high direction.
- Place items in quadrants only if the source gives enough signal.
- Use short quadrant titles and keep item labels inside their quadrant.
- State what each axis means and which direction is positive or higher.
- If placement is qualitative, group items in the right quadrant rather than inventing precise coordinates.
- Put ambiguous or insufficiently specified items near the center or leave them out with no fake precision.

Styling:
- Use subtle quadrant backgrounds and strong axis labels.
- Keep grid lines light.
- Avoid decorative icons and dense annotations.
- Use compact item chips and avoid overlap even if that makes the placement less exact.
```

## Funnel Prompt

Use for conversion, screening, narrowing, and staged reduction.

```text
Diagram type: funnel.

Layout:
- Use stacked horizontal bands or a stepped vertical funnel.
- Keep stages ordered from top to bottom.
- Include counts or rates only if the user supplied them.
- Make stage width meaningful only when quantitative values are provided.
- Preserve stage names and metric definitions exactly when supplied.
- If the source includes both volume and conversion rate, show the rate as secondary text under the count.
- If no numbers are supplied, use equal-width stage bands and focus on stage sequence, not fake proportions.

Styling:
- Use progressively lighter fills or decreasing widths.
- Place stage labels centered and details beneath or beside the stage.
- Highlight the largest drop-off only when the source gives enough quantitative evidence.
```

## Final Visual Review Prompt

Run this review mentally before accepting the SVG:

```text
Review the SVG as a visual design artifact:
- Is the layout balanced with clear margins and consistent spacing?
- Can every label be read at normal whiteboard zoom?
- Does any text overflow a node or collide with arrows?
- Are arrows routed cleanly without crossing important labels?
- Is the main story visible within 5 seconds?
- Does the palette use semantic contrast rather than random colors?
- Would this still look clean if imported onto a whiteboard canvas?

If any answer is no, revise the SVG before returning it.
```
