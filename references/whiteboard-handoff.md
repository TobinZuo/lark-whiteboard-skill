# Whiteboard Handoff

## Inputs To Provide Downstream

When invoking a Lark or Feishu whiteboard skill or tool, provide:

- `svg_path`: absolute path to the validated SVG file.
- `target_url`: Lark or Feishu document, wiki, or whiteboard URL, if supplied by the user.
- `title`: short board title.
- `mode`: prefer `editable-shapes` when supported; otherwise use `svg-import` or the closest supported SVG ingestion mode.
- `source_summary`: one or two sentences describing what the SVG represents.

## Expected Downstream Behavior

The whiteboard integration should:

- Authenticate with Lark or Feishu using its own configured credentials.
- Create or update the target board.
- Convert supported SVG shapes and text into whiteboard elements when possible.
- Fall back to importing the SVG as a single visual object only when editable conversion is unavailable.
- Return the final board URL or a clear failure reason.

## Failure Handling

If direct publishing fails:

1. Keep the validated SVG artifact.
2. Report the failure from the whiteboard integration.
3. Return the SVG path so the user can retry or import manually.

Do not claim a board was created unless the downstream tool returns a confirmed board URL or success result.
