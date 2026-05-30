# Content Enrichment Guide

Distilled from high-quality MindAI chart generation outputs. Use this guide to transform sparse user requests into information-rich, professional diagrams.

## Pre-generation Checklist

Before generating any diagram, verify the plan covers these four dimensions:

1. **Entities**: Are key nodes, modules, roles, or states named with specific labels?
2. **Relationships**: Are connections, call chains, data flows, or state transitions described?
3. **Scope boundaries**: Is it clear which systems, stages, or exception paths are in/out of scope?
4. **Key takeaways**: Are conclusions, risk points, bottlenecks, or metrics included?

If the user's request is sparse, enrich it using domain knowledge (see below). If the user provides specific structure, preserve it faithfully.

## Domain Knowledge Injection

When the user gives a vague topic, expand with industry-standard specifics:

| Diagram type | Expansion strategy | Example |
|---|---|---|
| Architecture | Add standard component names, tech stacks, protocols | "search engine" → Query Understanding, Retrieval (BM25+ANN), Ranking (LTR), Feature Cache (Redis), Inverted Index (ES) |
| Flowchart | Add exception branches, feedback loops, cross-role handoffs | "login flow" → credential validation failure retry, rate limiting, MFA challenge, session creation |
| Comparison | Add quantitative dimensions, recommendation badges | "cloud storage comparison" → SLA, concurrency, pricing tiers, capacity, recommended tier |
| Funnel | Add absolute values + inter-layer conversion rates | "conversion funnel" → Impressions 100K → Signup 42K (42%) → Cart 18K (43%) → Order 7.5K (42%) |
| Swimlane | Add cross-lane handoff semantics, request/response distinction | "ticket workflow" → Page/Escalate/Assign handoff labels, activation bars |

## Structural Decisions (Auto-apply)

Make these structural decisions automatically without requiring user specification:

- **Layering**: Organize flat components into 3-4 responsibility layers with named boundaries
- **Cross-cutting separation**: Isolate observability, security, governance into side/lower bands
- **Feedback loops**: Add feedback paths for closed-loop systems (data quality, A/B experiments, model updates)
- **Flow distinction**: Use solid lines for synchronous/request flow, dashed for async/batch/feedback

## Node Text Structure

Every node should have layered text, not just a bare label:

```
Pattern A: Title + Description (architecture preferred)
  Primary:   API Gateway              ← bold, component name
  Secondary: Rate limiting · Auth     ← gray, function or tech stack

Pattern B: Label + Metric (funnel/comparison preferred)
  Primary:   Submit Order             ← step name
  Metric:    7,500 users · 42% CVR   ← quantitative data

Pattern C: Number + Label + Purpose (process/flywheel preferred)
  Primary:   ③ Content Accumulation   ← numbered action
  Secondary: Build core traffic asset ← strategic significance
```

## Quantitative Enrichment

| Context | Add numbers? | What to add |
|---|---|---|
| Funnel/conversion | Always | Absolute values + conversion rates |
| Architecture deployment | Recommended | Replica counts (3 web, 5 API, 4 worker) |
| Comparison tables | Recommended | Concrete values per dimension, not vague descriptions |
| SLA/performance | Recommended | Percentages (99.9%) or latency (<50ms) |
| Conceptual flowcharts | No | Focus on logic, not measurement |
| Fishbone/causal | No | Focus on categorization, not quantification |
| Org charts | No | Focus on relationships, not metrics |

## Title and Subtitle

Every diagram should have a title area with both a main title and a subtitle:

| Diagram type | Subtitle content | Example |
|---|---|---|
| Architecture | Coverage scope or design principle | "Three-layer separation: real-time query · batch indexing · observability feedback loop" |
| Funnel | Analysis conclusion and action | "Cart-to-order stage shows highest drop-off, needs optimization" |
| Comparison | Evaluation purpose or recommendation logic | "Cloud storage selection guide based on team size and budget" |
| Flowchart | Process characteristics | "Payment closed-loop with exception handling and graceful degradation" |

## Per-Type Expansion Checklist

### Architecture
- Divide into 3-4 layers/zones with named responsibility boundaries
- Annotate each component with tech stack (specific product names)
- Label deployment nodes with replica counts
- Distinguish sync vs async paths visually
- Separate cross-cutting concerns into independent zone
- Use cylinder shapes for storage nodes
- Add legend when line styles encode different semantics

### Flowchart
- Group stages with background color blocks
- Identify and show feedback loops (dashed back-edges)
- Label connectors with action verbs
- Mark critical decision points or bottlenecks with emphasis
- Distinguish main flow (solid) from exception flow (dashed)

### Comparison
- Use 4-6 evaluation dimensions with concrete values
- Mark recommended option (badge + color emphasis)
- Attach target user description to each column
- Use prominent font size for pricing row

### Funnel
- Label each layer with absolute value + conversion rate
- Identify highest-loss stage, mark with red/warning
- Include optimization suggestion in subtitle
- Layer widths proportional to conversion

### Swimlane
- Define 3-5 roles with distinct color themes
- Label cross-lane handoffs with transfer semantics
- Distinguish request (solid arrow) from response (dashed arrow)
- Number steps to indicate execution order

## Information Density Guidelines

| Diagram type | Recommended nodes | Density | Text detail |
|---|---|---|---|
| Architecture | 14-28 | High | Label + description + metrics |
| Flowchart | 9-16 | Medium | Label + verb connectors |
| Comparison | 3-6 cols × 4-6 rows | Medium | Label + concrete values |
| Funnel | 4-6 layers | Medium | Label + dual metrics |
| Swimlane | 8-12 steps | Medium | Label + handoff annotations |
| Flywheel | 4-6 nodes | Low-Medium | Label + strategic explanation |
| Fishbone | 12-16 causes | Medium | Labels only |
| Org chart | 4-8 cards | Low-Medium | Label + description |

**Golden rule**: No node should exceed 3 lines of text. If it does, split into primary label + secondary annotation. Prioritize readability over completeness.
