# Handoff

The active batch is `ELP-VERIFY-REPLAY-01`, authorized by merged Portfolio Control
PR #501 at `1713665398b4d570611e7e8e19195d25fb8b7b38`. It starts from target
`01a510244801cbf2c3b7ce990693aac9dc5959c1`, where DSP P11-P20 was already merged.

This repair changes only validation and its activation/evidence documents.
Fixture replay has a strict per-component portability allowance capped at one
percent of the existing scientific budget and `1e-9 * max(1, abs(saved))`.
Fresh production/reference comparisons retain their original scientific gates.
Historical GNC error metadata is checked against the immutable saved pair.
DSP regressions check the exact retained P11-P20 contract, so later batch
activation does not invalidate completed work.

See `docs/evidence/ELP-VERIFY-REPLAY-01-2026-09-26.md` for baseline failures,
read-only audit, negative controls, verification results, and rollback.
Target protected-branch merge still requires human approval. After this repair
merges, reissue the control P21-P28 contract against the exact resulting commit
and tree before activating that manually gated batch.

Issue 441 remains open. The repair ledger remains P01 distinct, P02-P10 repaired,
P11-P20 repaired, and P21-P84 pending. The catalog remains six courses,
290 modules, and 290 interactive modules. Preserve the exact DSP gitlink,
source map, conversion manifest, coverage and maturity claims.

MATLAB runtime comparison, audio playback, browser/accessibility, learner
validation, physical HIL/hardware, certification, release, deployment,
credentials/settings, and production evidence remain unperformed.
