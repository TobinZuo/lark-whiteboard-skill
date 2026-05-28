# Layout Recipes

Use these numeric recipes to keep generated SVG diagrams polished and readable.

## Layout Rule

Before placing nodes, choose one layout archetype from [layout-archetypes.md](layout-archetypes.md) and keep it consistent throughout the diagram.

## Canvas

- Default canvas: `1600 x 1000`.
- Compact diagram: `1200 x 800`, only when there are fewer than 8 nodes.
- Dense diagram: `1800 x 1100`, only when needed for 12 to 24 nodes.
- Outer margin: 72 px for large canvases, 56 px for compact canvases.
- Grid: 24 px. Align node x/y positions and major connectors to this grid.

## Node Dimensions

- Small process step: `220 x 96`.
- Standard service or concept node: `260 x 120`.
- Wide stage card: `320 x 132`.
- Lane step card: `240 x 96`.
- Participant header in sequence diagrams: `220 x 72`.
- Matrix item chip: `180 x 52`.

Keep repeated nodes exactly the same size within a diagram type unless the user explicitly asks to emphasize one node.

## Spacing

- Horizontal gap between same-level nodes: 64 to 96 px.
- Vertical gap between same-level rows: 56 to 80 px.
- Gap between grouped zones: 96 to 140 px.
- Text padding inside nodes: at least 16 px left/right and 14 px top/bottom.
- Arrow clearance from text: at least 18 px.

## Palette

Use a restrained, semantic palette. Pick only colors that encode meaning:

- Canvas: `#ffffff` or `#f8fafc`.
- Text primary: `#17202c`.
- Text secondary: `#4b5563`.
- Neutral stroke: `#64748b`.
- Primary path: `#2563eb`.
- Data or storage: `#0f766e`.
- Success: `#2f7d4f`.
- Warning: `#b7791f`.
- Risk or blocker: `#b42318`.
- Group fill: light tints such as `#f1f5f9`, `#eef6ff`, `#edf7f2`, `#fff7e6`.

Avoid purple-heavy, dark-blue-heavy, beige-only, or one-hue palettes.

## Typography

- Title: 44 px, semibold visual weight through color or size.
- Subtitle or context note: 20 px.
- Section/lane label: 26 px.
- Node main label: 24 px.
- Node secondary label: 18 px.
- Edge label: 16 to 18 px.

Never reduce readable labels below 16 px. Simplify text or increase the canvas instead.

## Architecture Recipe

- Use one of these skeletons:
  - left-right pipeline for request serving
  - top-down stack for platform layers
  - split-band for online plus offline paths
  - hub-and-spoke for central coordinator designs
- Give each semantic tier a fixed band or column.
- Keep primary request/data flow on one clearly visible axis.
- Put storage below or beside owning service, not floating far away.
- Keep external dependencies outside the core band.
- Use one primary colored path; keep secondary dependencies gray.
- If the diagram has both online and offline logic, separate them into bands or rows instead of mixing them.
- Keep monitoring, alerting, analytics, and ops feedback loops in a separate side band.

## Component Recipe

- Use 3 to 5 horizontal or vertical layers.
- Put public interfaces, controllers, handlers, or SDK APIs at the entry layer.
- Put domain, orchestration, policy, or core modules in the center.
- Put adapters, clients, storage, queues, and external integrations at the edge.
- Keep package or repository boundaries as light group boxes with clear labels.

## Deployment Recipe

- Use nested boxes for cloud/region/VPC/cluster/namespace boundaries.
- Use entry points on the left/top boundary, workloads in the center, backing services on the right/bottom.
- Keep infrastructure boundary labels outside the workload cards.
- Use dashed outlines for optional, standby, or disaster recovery environments only when explicit.

## Data Flow Recipe

- Use columns: sources, ingestion, processing, storage, serving, consumers.
- Use parallel rows for batch and streaming flows.
- Put topic/table/file names on edges only if labels remain readable.
- Use storage-shaped cards consistently for queues, tables, buckets, warehouses, and caches.

## General Spacing Rule

- Keep unrelated bands at least 96 px apart.
- Keep nodes in the same band aligned to a shared baseline or centerline.
- If labels start to overlap, widen the canvas before shrinking text.
- Prefer more whitespace over denser placement.

## Flowchart Recipe

- Put the main path in one straight line.
- Put exceptions or failure paths to the side, using smaller cards if needed.
- Use diamonds only for true decisions.
- Keep branch labels outside the diamond and close to the outgoing edge.

## CI/CD Pipeline Recipe

- Use a left-to-right pipeline rail with 5 to 8 major stages.
- Put quality gates and approvals as smaller diamonds or gate cards between stages.
- Put rollback/failure paths below the main rail and route them to the target environment.
- Use compact badges for artifacts, images, branches, tags, or environments.

## Swimlane Recipe

- Use a fixed lane label column of 180 to 220 px.
- Use lane height of 140 to 180 px.
- Use alternating lane fills with very low contrast.
- Place steps by time from left to right; never center all steps if chronology matters.

## Sequence Recipe

- Participant columns should be evenly spaced.
- Lifelines start under participant headers and end near the last message.
- Use y-spacing of 72 to 96 px between messages.
- Use activation bars only if they clarify nested execution.

## State Machine Recipe

- Use a ring or left-to-right lifecycle layout depending on whether the machine loops.
- Put the initial state near the top-left or top-center.
- Put terminal success on the right and terminal failure/cancelled below the main path.
- Use curved connectors for retries and self-loops.
- Keep every transition labeled unless it is explicitly automatic.

## ER Diagram Recipe

- Use table cards sized around `280 x 180` to `340 x 260`.
- Use a 48 px header area for table names.
- Use 28 to 34 px field rows.
- Put key fields at the top with compact `PK` and `FK` tags.
- Use relationship lines from table edges for dense schemas, or from field rows for small schemas.

## Org Chart Recipe

- Use a centered root node and balanced subtree spacing.
- Keep every level on one y-coordinate.
- Use straight or orthogonal connectors.
- Avoid deep text in people/team cards; keep role details secondary.

## Timeline Recipe

- Use a strong horizontal axis with milestone markers.
- Alternate callouts above and below the axis only when markers are close.
- Use bars for durations, dots for point events.
- Preserve exact dates and labels; do not normalize vague phase names into fake dates.

## Mind Map Recipe

- Limit first-level branches to 4 to 8 visible directions.
- Use short curved or straight connectors from center to branch heads.
- Keep child nodes within the visual wedge of their branch.
- Split the map if more than 35 nodes are required.

## Matrix Recipe

- Use axis labels outside the plot area.
- Keep quadrant titles in the corners.
- Keep item chips short and avoid overlapping chips.
- If placement is uncertain, use the center of the relevant quadrant rather than inventing precision.

## Funnel Recipe

- Use stacked bands when exact numbers are unavailable.
- Use proportional widths only when counts or rates are supplied.
- Put count/rate text on a second line, not mixed into the stage title.
