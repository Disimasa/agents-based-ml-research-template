---
name: literature-survey
description: Discover phase — structured literature search with outline, fields, and JSON results
---

# Literature survey

**Phase:** `discover`  
**Agents:** `literature_scout`, `source_verifier`, `synthesis_agent`

## When to use

- Phase `discover` is enabled
- User asks for related work, literature review, or bibliography

## Prerequisites

- `runtime/state/passport.yaml` with `research_question`
- Template: `runtime/templates/literature_example/`

## Steps

### 1. Scope

- Choose `topic_slug` (e.g. `contrastive_reranking`)
- Create agent state: `runtime/state/literature/{topic_slug}/`
- Create user output: `research/literature/{topic_slug}/results/`

### 2. Outline (`runtime/state/literature/{topic}/outline.yaml`)

```yaml
topic: <topic_slug>
items:
  - id: item_001
    title: "<search theme>"
    query_hints: ["keywords", "authors"]
    priority: 1
execution:
  batch_size: 5
  items_per_agent: 1
  output_dir: research/literature/<topic_slug>/results
```

### 3. Fields (`runtime/state/literature/{topic}/fields.yaml`)

Define extraction schema per paper:

```yaml
fields:
  - name: method
    description: "Core approach"
    detail_level: moderate
  - name: metrics
    description: "Reported metrics and datasets"
    detail_level: detailed
  - name: limitations
    description: "Stated limitations"
    detail_level: brief
```

### 4. Search and record (`research/literature/{topic}/results/*.json`)

Per source batch, write JSON (user-facing source cards):

```json
{
  "id": "src_001",
  "title": "...",
  "year": 2024,
  "doi": "...",
  "url": "...",
  "verified": false,
  "fields": { "method": "...", "metrics": "..." },
  "notes": ""
}
```

### 5. Verify (`source_verifier`)

- Set `verified: true` only after DOI/URL check
- Deduplicate; log rejections in `research/decision_log.md`

### 6. Synthesize gaps (`synthesis_agent`)

- Optional `research/literature/{topic}/README.md` — gaps and trends for the user
- Update `runtime/state/passport.yaml` `claims[]` only from verified sources

### 7. State update

- `passport.phase: discover`
- Run `integrity-check` (M1)
- **HITL gate:** `pending_approval: true` until human approves literature pack

## Optional external tools

See `docs/REFERENCES.md` — Orchestra `paper-lookup`, K-Dense literature skills (MIT, optional install).

## Handoff

→ `hypothesis-ideation` (ideate)
