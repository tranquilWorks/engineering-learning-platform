# Component Model

The platform deliberately limits the native lesson vocabulary so course authors compose learning experiences instead of writing frontend code.

Version-one blocks and controls are discriminated, closed variants. A field
valid for one variant is not silently accepted on another. Labels are explicit,
result references use stable keys, and free-form values exist only in documented
content carriers.

## Narrative primitives

- Markdown and KaTeX
- prediction/reveal checkpoint
- state-dependent callout
- divider and section title
- optional media from module `assets/`
- allow-listed direct-manipulation widgets such as the two-parameter drag map

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

## Direct-manipulation widgets

The `widget` block references a platform-owned, allow-listed renderer. Course folders cannot inject arbitrary JavaScript. The foundation includes `parameter-map`, which binds an x/y drag probe to two numeric controls. Future built-ins can add vector probes, draggable geometry, matrix editors, constellation manipulators, signal-chain routing, and plot-selection tools without weakening the trust boundary.

`parameter-map` has exactly four properties in version one: distinct
`x_control` and `y_control` references to declared numeric controls plus
non-empty `x_label` and `y_label` text. An undeclared widget or property fails
catalog validation.
