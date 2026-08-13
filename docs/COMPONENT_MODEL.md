# Component Model

The platform deliberately limits the native lesson vocabulary so course authors compose learning experiences instead of writing frontend code.

## Narrative primitives

- Markdown and KaTeX
- prediction/reveal checkpoint
- state-dependent callout
- divider and section title
- optional media from module `assets/`

## Manipulation primitives

- continuous slider
- exact number input
- toggle/failure-mode switch
- select
- segmented comparison
- action/regenerate button

## Evidence primitives

- metric card
- Plotly figure
- linked plot grid
- dataframe-like table
- warning/diagnostic message

## Learning-loop template

```yaml
blocks:
  - type: markdown
    source: lesson.md
  - type: prediction
    text: What do you expect to change?
    reveal: State the expected causal relationship.
  - type: controls
  - type: metrics
  - type: plot
    plot: main
  - type: callout
    source: interpretation
  - type: plot_grid
    plots: [comparison_a, comparison_b]
  - type: table
    table: cases
  - type: callout
    tone: warning
    text: Name the interpretation boundary or broken model.
```

A future schema revision may add draggable geometry, direct plot annotations, quizzes, code fragments, video synchronization, and parameterized diagrams. Those should extend the same ordered block model rather than turn each lesson into custom React code.
