# Code-Gen Layout Guide

Generate diagrams by writing a Node.js layout script instead of hand-coding SVG coordinates. The script computes precise positions algorithmically, then renders SVG from templates. This produces pixel-perfect layouts comparable to dedicated diagram engines.

## When to Use Code-Gen

| Scenario | Approach |
|---|---|
| Simple diagram, < 10 nodes, linear flow | Direct SVG |
| Swimlane, multi-branch, grid alignment, ring/polar layout | **Code-gen script** |
| Architecture with precise layer alignment | **Code-gen script** |
| Any diagram where node overlap or misalignment is likely | **Code-gen script** |

## Script Structure (Three-Phase Pattern)

Every layout script follows this structure:

```javascript
const fs = require('fs');

// ═══════════════════════════════════════════
// PHASE 1: DATA — Define content and relationships
// ═══════════════════════════════════════════
const title = "...";
const subtitle = "...";
const lanes = [...];   // or layers, stages, nodes
const edges = [...];   // connections between nodes

// ═══════════════════════════════════════════
// PHASE 2: LAYOUT — Compute coordinates algorithmically
// ═══════════════════════════════════════════
// Constants
const LANE_H = 160, STAGE_W = 180, NODE_W = 140, NODE_H = 44, GAP = 20;
// ... coordinate calculations using loops and arithmetic

// ═══════════════════════════════════════════
// PHASE 3: RENDER — Assemble SVG string and write file
// ═══════════════════════════════════════════
const svg = `<svg xmlns="http://www.w3.org/2000/svg" ...>...</svg>`;
fs.writeFileSync('diagram.svg', svg);
console.log('Written: diagram.svg');
```

## Color Palette (Mandatory)

```javascript
const PALETTE = {
  blue:   { fill: '#F0F4FC', stroke: '#5178C6' },
  purple: { fill: '#EAE2FE', stroke: '#8569CB' },
  green:  { fill: '#DFF5E5', stroke: '#509863' },
  yellow: { fill: '#FEF1CE', stroke: '#D4B45B' },
  red:    { fill: '#FEE3E2', stroke: '#D25D5A' },
};
const TEXT_PRIMARY = '#1F2329';
const TEXT_SECONDARY = '#646A73';
const TEXT_MUTED = '#8F959E';
const LINE_COLOR = '#BBBFC4';
const BG_WHITE = '#FFFFFF';
```

## Typography Constants

```javascript
const FONT = 'Arial, Helvetica, sans-serif';
const TITLE_SIZE = 24;    // diagram title
const SUBTITLE_SIZE = 14; // diagram subtitle
const LABEL_SIZE = 14;    // node primary label
const DESC_SIZE = 12;     // node secondary description
const EDGE_LABEL_SIZE = 12; // connector labels
```

## SVG Rendering Helpers

Include these in every script:

```javascript
function svgRect(x, y, w, h, {fill = BG_WHITE, stroke = LINE_COLOR, strokeWidth = 2, rx = 6} = {}) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"/>`;
}

function svgText(x, y, text, {size = LABEL_SIZE, color = TEXT_PRIMARY, anchor = 'middle', weight = 'normal'} = {}) {
  return `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${size}" font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${text}</text>`;
}

function svgDiamond(cx, cy, w, h, {fill = BG_WHITE, stroke = LINE_COLOR, strokeWidth = 2} = {}) {
  const points = `${cx},${cy-h/2} ${cx+w/2},${cy} ${cx},${cy+h/2} ${cx-w/2},${cy}`;
  return `<polygon points="${points}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"/>`;
}

function svgEllipse(cx, cy, rx, ry, {fill = BG_WHITE, stroke = LINE_COLOR, strokeWidth = 2} = {}) {
  return `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"/>`;
}

function svgArrowMarker(id, color) {
  return `<marker id="${id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
    <path d="M 0 1 L 8 5 L 0 9 z" fill="${color}"/>
  </marker>`;
}

function svgPolyline(points, {stroke = LINE_COLOR, strokeWidth = 1.5, marker = '', dash = ''} = {}) {
  const pts = points.map(p => p.join(',')).join(' ');
  let attrs = `fill="none" stroke="${stroke}" stroke-width="${strokeWidth}"`;
  if (marker) attrs += ` marker-end="url(#${marker})"`;
  if (dash) attrs += ` stroke-dasharray="${dash}"`;
  return `<polyline points="${pts}" ${attrs}/>`;
}
```

## Layout Algorithm Templates

### Swimlane Grid (Flowchart with Roles)

Use when: login flow, approval flow, cross-system interaction, any multi-actor process.

```javascript
// Data
const lanes = [
  { id: 'client', label: '用户端 / 前端', color: PALETTE.blue },
  { id: 'server', label: '服务端 / 逻辑层', color: PALETTE.green },
  { id: 'data',   label: '数据层 / 持久化', color: PALETTE.yellow },
];

const steps = [
  // [laneIndex, stageIndex, label, sublabel, options]
  [0, 0, '访问应用主页', '', {}],
  [0, 1, '操作选择', '', { shape: 'diamond' }],
  [0, 2, '输入登录凭证', '', {}],
  [1, 3, '风控与参数校验', '', {}],
  [1, 4, '查询与比对凭证', '', {}],
  [1, 5, '凭证正确?', '', { shape: 'diamond' }],
  // ...
];

const edges = [
  // [fromStepIdx, toStepIdx, label, options]
  [0, 1, '', {}],
  [1, 2, '已有账号', {}],
  [5, 6, '凭证正确', { color: PALETTE.green.stroke }],
  [5, 7, '凭证错误', { color: PALETTE.red.stroke, dash: true }],
  // ...
];

// Layout calculation
const HEADER_H = 80;           // title area
const LANE_LABEL_W = 130;      // lane label column width
const LANE_H = 180;            // each lane height
const STAGE_W = 160;           // each stage column width
const NODE_W = 128, NODE_H = 44;
const LANE_GAP = 8;

const canvasW = LANE_LABEL_W + stages.length * STAGE_W + 40;
const canvasH = HEADER_H + lanes.length * (LANE_H + LANE_GAP) + 40;

// Compute node center positions
function nodeCenter(laneIdx, stageIdx) {
  const x = LANE_LABEL_W + stageIdx * STAGE_W + STAGE_W / 2;
  const y = HEADER_H + laneIdx * (LANE_H + LANE_GAP) + LANE_H / 2;
  return { x, y };
}
```

### Layered Band (Architecture Diagram)

Use when: system architecture, service layers, infrastructure topology.

```javascript
const layers = [
  { label: '接入层', labelEn: 'Access Layer', color: PALETTE.blue, nodes: [...] },
  { label: '服务层', labelEn: 'Service Layer', color: PALETTE.purple, nodes: [...] },
  { label: '存储层', labelEn: 'Data Layer', color: PALETTE.yellow, nodes: [...] },
];

const LAYER_H = 120;
const LAYER_GAP = 16;
const LABEL_W = 140;
const NODE_W = 160, NODE_H = 56;
const PADDING = 40;

const canvasW = 1200;

layers.forEach((layer, i) => {
  layer.y = PADDING + 80 + i * (LAYER_H + LAYER_GAP);
  const contentW = canvasW - PADDING * 2 - LABEL_W - 20;
  const nodeGap = (contentW - layer.nodes.length * NODE_W) / (layer.nodes.length + 1);
  layer.nodes.forEach((node, j) => {
    node.x = PADDING + LABEL_W + 20 + nodeGap * (j + 1) + j * NODE_W;
    node.y = layer.y + (LAYER_H - NODE_H) / 2;
  });
});
```

### Topological Flow (DAG without external engine)

Use when: complex branching with merge points, state machines, decision trees.

```javascript
// Simple rank-based layout (no external dagre dependency)
// 1. Assign ranks (topological sort)
// 2. Within each rank, distribute nodes evenly on the cross-axis
// 3. Route edges as orthogonal polylines

function assignRanks(nodes, edges) {
  const inDegree = {};
  const adjList = {};
  nodes.forEach(n => { inDegree[n.id] = 0; adjList[n.id] = []; });
  edges.forEach(([from, to]) => { inDegree[to]++; adjList[from].push(to); });
  
  const queue = nodes.filter(n => inDegree[n.id] === 0).map(n => n.id);
  const rank = {};
  while (queue.length) {
    const id = queue.shift();
    rank[id] = rank[id] || 0;
    adjList[id].forEach(to => {
      rank[to] = Math.max(rank[to] || 0, rank[id] + 1);
      if (--inDegree[to] === 0) queue.push(to);
    });
  }
  return rank;
}

// Position nodes
const RANK_SEP = 200;  // horizontal distance between ranks
const NODE_SEP = 80;   // vertical distance between nodes in same rank

function positionNodes(nodes, rankMap) {
  const byRank = {};
  nodes.forEach(n => {
    const r = rankMap[n.id];
    (byRank[r] = byRank[r] || []).push(n);
  });
  Object.entries(byRank).forEach(([r, group]) => {
    const totalH = group.length * NODE_H + (group.length - 1) * NODE_SEP;
    const startY = (canvasH - totalH) / 2;
    group.forEach((n, i) => {
      n.x = PADDING + parseInt(r) * RANK_SEP;
      n.y = startY + i * (NODE_H + NODE_SEP);
    });
  });
}
```

### Polar Ring (Flywheel / Cycle)

Use when: growth flywheel, feedback loops, circular processes.

```javascript
const stages = [...]; // 4-6 items
const cx = canvasW / 2, cy = canvasH / 2;
const radius = 220;

stages.forEach((s, i) => {
  const angle = -90 + i * (360 / stages.length);
  const rad = angle * Math.PI / 180;
  s.x = cx + radius * Math.cos(rad) - NODE_W / 2;
  s.y = cy + radius * Math.sin(rad) - NODE_H / 2;
});

// Arc arrows between adjacent stages
function arcPath(i, j, r) {
  const a1 = (-90 + i * (360 / stages.length) + 15) * Math.PI / 180;
  const a2 = (-90 + j * (360 / stages.length) - 15) * Math.PI / 180;
  const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
  const x2 = cx + r * Math.cos(a2), y2 = cy + r * Math.sin(a2);
  return `M ${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2}`;
}
```

## Edge Routing (Orthogonal Polylines)

Always use orthogonal (right-angle) routing for connectors:

```javascript
function routeEdge(fromNode, toNode, fromSide = 'right', toSide = 'left') {
  const from = anchorPoint(fromNode, fromSide);
  const to = anchorPoint(toNode, toSide);
  
  if (fromSide === 'right' && toSide === 'left') {
    const midX = (from.x + to.x) / 2;
    return [[from.x, from.y], [midX, from.y], [midX, to.y], [to.x, to.y]];
  }
  if (fromSide === 'bottom' && toSide === 'top') {
    const midY = (from.y + to.y) / 2;
    return [[from.x, from.y], [from.x, midY], [to.x, midY], [to.x, to.y]];
  }
  // fallback: direct with one bend
  return [[from.x, from.y], [from.x, to.y], [to.x, to.y]];
}

function anchorPoint(node, side) {
  const cx = node.x + NODE_W / 2, cy = node.y + NODE_H / 2;
  switch (side) {
    case 'left':   return { x: node.x, y: cy };
    case 'right':  return { x: node.x + NODE_W, y: cy };
    case 'top':    return { x: cx, y: node.y };
    case 'bottom': return { x: cx, y: node.y + NODE_H };
  }
}
```

## Complete Example: User Login Swimlane Flowchart

This example produces output comparable to MindAI's swimlane diagrams:

```javascript
const fs = require('fs');

// ═══ PALETTE & HELPERS ═══
const PALETTE = {
  blue:   { fill: '#F0F4FC', stroke: '#5178C6' },
  green:  { fill: '#DFF5E5', stroke: '#509863' },
  yellow: { fill: '#FEF1CE', stroke: '#D4B45B' },
  red:    { fill: '#FEE3E2', stroke: '#D25D5A' },
};
const TEXT_PRIMARY = '#1F2329';
const TEXT_SECONDARY = '#646A73';
const LINE_COLOR = '#BBBFC4';
const FONT = 'Arial, Helvetica, sans-serif';

function svgRect(x, y, w, h, opts = {}) {
  const {fill='#FFFFFF',stroke=LINE_COLOR,sw=2,rx=6} = opts;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
}
function svgText(x, y, text, opts = {}) {
  const {size=14,color=TEXT_PRIMARY,anchor='middle',weight='normal'} = opts;
  return `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${size}" font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${text}</text>`;
}
function svgDiamond(cx, cy, w, h, opts = {}) {
  const {fill='#FFFFFF',stroke=LINE_COLOR,sw=2} = opts;
  return `<polygon points="${cx},${cy-h/2} ${cx+w/2},${cy} ${cx},${cy+h/2} ${cx-w/2},${cy}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
}

// ═══ 1. DATA ═══
const title = '用户注册登录流程';
const subtitle = '覆盖登录与注册双路径 · 含风控校验、凭证重试与账号冲突检测';

const lanes = [
  { label: '用户端 / 前端', color: PALETTE.blue },
  { label: '服务端 / 逻辑层', color: PALETTE.green },
  { label: '数据层 / 持久化', color: PALETTE.yellow },
];

// steps: [laneIdx, stageIdx, id, label, sublabel, shape]
const steps = [
  [0, 0, 'start',       '访问应用主页', '',             'rect'],
  [0, 1, 'choice',      '操作选择',    '',             'diamond'],
  [0, 2, 'login_input', '输入登录凭证', '',             'rect'],
  [0, 2, 'reg_input',   '输入注册信息', '',             'rect'],  // same stage, different lane handled below
  [1, 3, 'risk_check',  '风控与参数校验','频率+IP检测', 'rect'],
  [1, 4, 'query_cred',  '查询与比对凭证','密码哈希比对','rect'],
  [1, 5, 'cred_judge',  '凭证正确?',   '',             'diamond'],
  [1, 6, 'gen_token',   '生成鉴权Token','JWT签发',     'rect'],
  [0, 7, 'fail_tip',    '提示校验失败', '',             'rect'],
  [2, 6, 'cache_sess',  '缓存Session', 'Redis写入',    'rect'],
  [0, 8, 'login_done',  '登录成功主页', '',             'rect'],
  // Registration path
  [1, 3, 'fmt_check',   '格式校验与防刷','验证码校验', 'rect'],
  [1, 4, 'dup_check',   '查询账号存在性','',           'rect'],
  [1, 5, 'dup_judge',   '账号已存在?',  '',            'diamond'],
  [1, 6, 'hash_store',  '密码加盐与落库','bcrypt加密', 'rect'],
  [2, 6, 'write_db',    '写入新用户表', 'MySQL INSERT','rect'],
  [0, 7, 'conflict_tip','提示账号已存在','引导去登录',  'rect'],
  [0, 8, 'reg_done',    '注册成功引流', '',             'rect'],
];

// ═══ 2. LAYOUT ═══
const HEADER_H = 76;
const LANE_LABEL_W = 130;
const LANE_H = 140;
const LANE_GAP = 8;
const STAGE_W = 150;
const NODE_W = 128, NODE_H = 44;
const numStages = 9;

const canvasW = LANE_LABEL_W + numStages * STAGE_W + 60;
const canvasH = HEADER_H + lanes.length * (LANE_H + LANE_GAP) + 40;

function stageX(stageIdx) { return LANE_LABEL_W + stageIdx * STAGE_W + STAGE_W / 2; }
function laneY(laneIdx) { return HEADER_H + laneIdx * (LANE_H + LANE_GAP) + LANE_H / 2; }

// ═══ 3. RENDER ═══
let elements = [];

// Background
elements.push(svgRect(0, 0, canvasW, canvasH, {fill:'#FFFFFF', stroke:'none', sw:0, rx:0}));

// Title
elements.push(svgText(40, 34, title, {size:24, weight:'bold', anchor:'start'}));
elements.push(svgText(40, 56, subtitle, {size:14, color:TEXT_SECONDARY, anchor:'start'}));

// Lane backgrounds and labels
lanes.forEach((lane, i) => {
  const y = HEADER_H + i * (LANE_H + LANE_GAP);
  // Lane background
  elements.push(svgRect(LANE_LABEL_W, y, canvasW - LANE_LABEL_W - 20, LANE_H, {fill: lane.color.fill, stroke: lane.color.stroke, sw: 1.5, rx: 8}));
  // Lane label pill
  elements.push(svgRect(20, y + LANE_H/2 - 15, LANE_LABEL_W - 30, 30, {fill: lane.color.stroke, stroke:'none', sw:0, rx:4}));
  elements.push(svgText(20 + (LANE_LABEL_W-30)/2, y + LANE_H/2 + 5, lane.label, {size:13, weight:'bold', color:'#FFFFFF'}));
  // Lane divider (dashed)
  if (i < lanes.length - 1) {
    const divY = y + LANE_H + LANE_GAP / 2;
    elements.push(`<line x1="${LANE_LABEL_W}" y1="${divY}" x2="${canvasW-20}" y2="${divY}" stroke="#DEE0E3" stroke-width="1" stroke-dasharray="4 4"/>`);
  }
});

// Nodes
steps.forEach(([laneIdx, stageIdx, id, label, sublabel, shape]) => {
  const cx = stageX(stageIdx);
  const cy = laneY(laneIdx);
  
  if (shape === 'diamond') {
    elements.push(svgDiamond(cx, cy, 100, 64, {fill: PALETTE.yellow.fill, stroke: PALETTE.yellow.stroke}));
    elements.push(svgText(cx, cy + 5, label, {size:13, weight:'bold'}));
  } else {
    const x = cx - NODE_W/2, y = cy - NODE_H/2;
    const isError = id.includes('fail') || id.includes('conflict');
    const color = isError ? PALETTE.red : lanes[laneIdx].color;
    elements.push(svgRect(x, y, NODE_W, NODE_H, {fill:'#FFFFFF', stroke: color.stroke, sw:2}));
    elements.push(svgText(cx, sublabel ? cy - 2 : cy + 5, label, {size:14, weight:'bold'}));
    if (sublabel) {
      elements.push(svgText(cx, cy + 14, sublabel, {size:11, color: TEXT_SECONDARY}));
    }
  }
});

// Arrow marker
elements.unshift(`<defs>${[
  `<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 8 5 L 0 9 z" fill="${LINE_COLOR}"/></marker>`
].join('')}</defs>`);

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${canvasW}" height="${canvasH}" viewBox="0 0 ${canvasW} ${canvasH}">\n${elements.join('\n')}\n</svg>`;
fs.writeFileSync('diagram.svg', svg);
console.log(`Written: diagram.svg (${canvasW}x${canvasH})`);
```

## Execution

After generating the script:

```bash
node diagram.gen.cjs
python3 scripts/validate_svg.py diagram.svg
```

If validation fails, fix the script and re-run. The script is the source of truth, not the SVG.

## Key Principles

1. **Never hand-write coordinates** — all positions must be computed from layout constants
2. **Grid-first** — establish the grid (lanes × stages, layers × columns) before placing any node
3. **Consistent sizing** — nodes in the same role use the same width/height
4. **Orthogonal routing** — connectors use horizontal and vertical segments only
5. **Semantic color** — color encodes meaning (role, status, emphasis), not decoration
6. **Compact nodes** — prefer 128×44 over 200×108; information density matters
7. **Two-line nodes** — every non-trivial node has a primary label + secondary description
