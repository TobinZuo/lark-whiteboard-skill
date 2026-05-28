# SVG Guidelines

## Supported Shape Set

Use portable SVG that can be parsed and converted by downstream whiteboard tools:

- Root: `svg`
- Groups and metadata: `g`, `title`, `desc`, `defs`, `marker`
- Shapes: `rect`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `path`
- Text: `text`, `tspan`

Avoid `script`, `foreignObject`, `iframe`, `object`, `embed`, `audio`, `video`, `canvas`, and external `image` references.

## Required Root Attributes

Every generated SVG must include:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">
```

Use a positive numeric `width`, `height`, and `viewBox`. Choose canvas dimensions that match the diagram:

- Small flow or org chart: `1200 x 800`
- Architecture or swimlane diagram: `1600 x 1000`
- Dense system map or timeline: `1800 x 1100`

## Text

- Use `<text>` elements so labels can remain editable when supported.
- Set `font-family` to a generic stack such as `Arial, Helvetica, sans-serif`.
- Use a type scale instead of arbitrary font sizes:
  - Title: 40 to 52 px.
  - Section or lane labels: 24 to 32 px.
  - Node labels: 20 to 28 px.
  - Secondary annotations: 16 to 20 px.
- Use no more than two lines inside compact nodes and no more than three lines inside large cards.
- Use `tspan` for manual wrapping.
- Keep at least 12 px horizontal padding and 10 px vertical padding around text inside a node.

## Styling

- Inline critical presentation attributes or use internal CSS that does not contain `url()`, `@import`, or external references.
- Use high-contrast fill/stroke combinations.
- Use stroke widths between 2 and 4 for normal shapes and 4 to 6 for major flows.
- Use marker arrowheads for directed edges.
- Use a neutral canvas background such as `#ffffff`, `#f8fafc`, or no background.
- Use no more than five semantic colors per diagram:
  - Primary path: blue or teal.
  - Success or completed state: green.
  - Warning or risk: amber.
  - Error or blocker: red.
  - Neutral groups and secondary paths: gray.
- Avoid heavy gradients, drop shadows, glass effects, 3D effects, clip-path decoration, and decorative blobs.

## Layout

- Keep at least 32 px between related nodes and at least 48 px between unrelated groups.
- Leave outer margins of at least 48 px on small canvases and 72 px on large canvases.
- Align nodes to a visible grid, usually 20 px or 24 px.
- Keep arrows from crossing labels.
- Group related subsystems with light boundary boxes only when grouping clarifies the diagram.
- Put legends in a corner only when symbols or colors encode meaning.
- Route arrows orthogonally for structured diagrams unless a curved connector materially improves readability.
- Keep the main reading path visually dominant through position, color, or stroke weight.
- Prefer simplifying or splitting dense content over shrinking text below 16 px.

## Quality Gate

Before handoff, inspect the generated SVG against these checks:

- No text overflows its container.
- No label is hidden behind an arrow or shape.
- The main reading order is obvious.
- Similar elements have identical dimensions unless there is a semantic reason.
- Related elements are grouped by proximity and alignment, not only by color.
- The diagram still looks clear when scaled to a whiteboard viewport.

## Accessibility

Add a short `<title>` and `<desc>` under the root `svg` for non-trivial diagrams. The description should summarize the diagram's purpose, not repeat every label.
