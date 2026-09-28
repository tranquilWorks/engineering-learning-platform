# Handoff

The owner approved merging PR #49 and starting the next grouping on 2026-09-28.
PR #49 merged as `e28b041aff3f4e66cec2190e04a5d689be23f260`, tree
`4b3ee5c371db2835920c4c3d8b04cd29dab2954b`. Control PR #519 merged as
`f808efb4c719b884e63c670d4e064e1855f7b5cb`; the active contract is an exact copy.

Branch: `codex/dsp-fidelity-p65-p76-20260928` in the isolated ELP worktree.
All twelve P65-P76 experiments, native lessons and sixty independent comparisons
are implemented. Numerical replay passed 1e-8 absolute/scaled-relative limits,
maximum absolute difference 1.223725121235475e-09. Required broader verification
is in progress; do not claim full validation or target merge yet.

Inputs preserve private source generator formulas and column-major ordering;
P65-P72 split uniform radius/phase blocks, P73-P76 interleave them. P75 shorter
apertures crop the full baseline noise record to keep input changes isolated.
This is deterministic software evidence, not MATLAB execution. Prior reference
bytes and all earlier module files remain unchanged. DSP source stays clean at
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`.

Ledger: one distinct, sixty-three prior repairs, twelve current repairs, eight
pending. P77-P84 and whole-course numerical/curriculum/capstone maturity remain
blocked; issue 441 stays open. The next proposed group is the final eight
P77-P84, after this batch's merge and a fresh scoped contract.

Protected target merge requires separate approval; current approval covered #49.
Hosted CI is nonmandatory under retained owner direction; local gates remain
mandatory. Preserve source/history checkout limitations and all runtime limits.
Use `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` for serialized
verification. No MATLAB, browser/accessibility, representative learner, hardware,
deployment or production claim. Refresh the existing local preview after the
verified build completes.
