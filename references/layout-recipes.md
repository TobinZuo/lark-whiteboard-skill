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

## Connector Routing

- Use orthogonal connectors by default: horizontal and vertical segments with clear bend points.
- Keep primary flow connectors short and aligned to the main reading direction.
- Route feedback, exception, monitoring, safety, and rollback paths along the outer edge of the relevant band or lane.
- Avoid long sweeping curves across the canvas; use curves only for compact loops, retries, or state transitions where the curve makes the relationship clearer.
- Do not run connectors through node bodies, over labels, behind section headers, or through unrelated bands.
- When several connectors return to an earlier stage, use a shared return rail near the band edge instead of separate crossing arcs.

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
- Use one size for peer components, usually `240 x 96` or `260 x 112`.
- Route dependencies layer-to-layer; avoid dependency lines that cross package headers.
- Put cross-cutting modules in a narrow side column only when they are used by many layers.

## Deployment Recipe

- Use nested boxes for cloud/region/VPC/cluster/namespace boundaries.
- Use entry points on the left/top boundary, workloads in the center, backing services on the right/bottom.
- Keep infrastructure boundary labels outside the workload cards.
- Use dashed outlines for optional, standby, or disaster recovery environments only when explicit.
- Use large boundary padding of at least 32 px between nested scopes.
- Keep public entry points on the outer boundary and private workloads inside the network or cluster boundary.
- Put managed services in a separate backing-services column or bottom band.

## Data Flow Recipe

- Use columns: sources, ingestion, quality gates, processing, storage maturity, semantic/serving, consumers.
- Use storage maturity stages when applicable: raw landing, staged/clean, curated warehouse, metric marts, semantic layer.
- Use parallel rows for streaming and batch flows; use a slim lower band for orchestration, catalog, lineage, and data quality feedback.
- Put topic, table, file, or metric names on edges only if labels remain readable.
- Use storage-shaped cards consistently for queues, object stores, lakes, tables, warehouses, marts, indexes, feature stores, and caches.
- Show quality checks before trusted storage, not after the dashboard.
- Place dashboards at the far right and label them by audience or decision, such as executive KPIs, product analytics, finance reporting, or operational monitoring.
- If the diagram is about "ingestion to warehouse to dashboard", emphasize the handoff from raw ingestion to trusted warehouse tables and then to semantic metrics.

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
- Use `220 x 96` stage cards and `180 x 110` decision diamonds as a default scale.
- Keep exception paths visually thinner or lower contrast than the happy path.
- Keep terminal states aligned at the end of their path.

## CI/CD Pipeline Recipe

- Use a left-to-right pipeline rail with 5 to 8 major stages.
- Put quality gates and approvals as smaller diamonds or gate cards between stages.
- Put rollback/failure paths below the main rail and route them to the target environment.
- Use compact badges for artifacts, images, branches, tags, or environments.
- Group by responsibility bands such as Source, CI, Artifact, Staging, Production, Verify.
- Use a lower rollback rail only when rollback or failure handling is explicit.
- Keep environment cards wider than individual job cards so promotion is visually clear.

## Swimlane Recipe

- Use a fixed lane label column of 180 to 220 px.
- Use lane height of 140 to 180 px.
- Use alternating lane fills with very low contrast.
- Place steps by time from left to right; never center all steps if chronology matters.
- Align handoff arrows to lane midlines where possible.
- Keep each lane to 3 to 7 visible steps; split dense workflows into phases.
- Use a top time/phase ruler when there are many handoffs.

## Sequence Recipe

- Participant columns should be evenly spaced.
- Lifelines start under participant headers and end near the last message.
- Use y-spacing of 72 to 96 px between messages.
- Use activation bars only if they clarify nested execution.
- Keep message arrows horizontal; use notes or brackets for optional sections instead of diagonal connectors.
- Reserve at least 160 px between participant centerlines for readable message labels.
- Put async/event messages in a subtly different stroke only when the source distinguishes them.

## State Machine Recipe

- Use a ring or left-to-right lifecycle layout depending on whether the machine loops.
- Put the initial state near the top-left or top-center.
- Put terminal success on the right and terminal failure/cancelled below the main path.
- Use curved connectors for retries and self-loops.
- Keep every transition labeled unless it is explicitly automatic.
- Use a main lifecycle row and a lower exception/retry row for business workflows.
- Keep retry loops small and close to the state they retry.
- Put manual intervention states in a side cluster when they are not on the main lifecycle.

## ER Diagram Recipe

- Use table cards sized around `280 x 180` to `340 x 260`.
- Use a 48 px header area for table names.
- Use 28 to 34 px field rows.
- Put key fields at the top with compact `PK` and `FK` tags.
- Use relationship lines from table edges for dense schemas, or from field rows for small schemas.
- Place central transaction or fact tables near the center, dimensions or lookup tables around them.
- Keep relationship labels outside table bodies.
- Use table-edge connectors for schemas with more than 5 relationships.

## Org Chart Recipe

- Use a centered root node and balanced subtree spacing.
- Keep every level on one y-coordinate.
- Use straight or orthogonal connectors.
- Avoid deep text in people/team cards; keep role details secondary.
- Use `220 x 88` cards for people and `260 x 96` cards for teams by default.
- Keep dotted advisory lines outside the main reporting tree.
- Split very wide teams into grouped subtrees rather than shrinking card text.

## Timeline Recipe

- Use a strong horizontal axis with milestone markers.
- Alternate callouts above and below the axis only when markers are close.
- Use bars for durations, dots for point events.
- Preserve exact dates and labels; do not normalize vague phase names into fake dates.
- Use stacked lanes when parallel workstreams matter.
- Use even phase spacing when the source uses phases instead of exact dates.
- Keep callouts short and put details in a second line.

## Mind Map Recipe

- Limit first-level branches to 4 to 8 visible directions.
- Use short curved or straight connectors from center to branch heads.
- Keep child nodes within the visual wedge of their branch.
- Split the map if more than 35 nodes are required.
- Use larger branch-head nodes than leaf nodes.
- Use one color per first-level branch and a lighter fill for its children.
- Keep child levels radially ordered so branches do not interleave.

## Matrix Recipe

- Use axis labels outside the plot area.
- Keep quadrant titles in the corners.
- Keep item chips short and avoid overlapping chips.
- If placement is uncertain, use the center of the relevant quadrant rather than inventing precision.
- Leave at least 24 px padding inside each quadrant for labels and chips.
- Put ambiguous items near the axis intersection instead of forcing them into a corner.
- Use consistent chip size unless item importance is explicitly encoded.

## Funnel Recipe

- Use stacked bands when exact numbers are unavailable.
- Use proportional widths only when counts or rates are supplied.
- Put count/rate text on a second line, not mixed into the stage title.
- Use a side annotation column for explanations, drop-off reasons, or owners when supplied.
- Keep each stage height consistent unless counts are explicitly represented by area.
- Use neutral colors for stages and reserve warning color for an evidenced drop-off.
