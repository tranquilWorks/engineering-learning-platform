# Handoff

The owner requested the final group on 2026-09-28 after the PR #50 merge and
continuation handoff. PR #50 merged as
`f05403ef2c0a5e31d7045c0cb796b2e136ca50c9`, tree
`f30d2a4a74d1fb76b94c6446095698615847cbbb`. Control PR #523 merged as
`d0c6bc74992a1e62aa6f372334be5f7a079a20ec`; the active contract is an exact copy.

Branch: `codex/dsp-fidelity-p77-p84-20260928` in the isolated ELP worktree.
All eight P77-P84 experiments, native lessons and forty retained independent
comparisons are implemented. Numerical replay passes 1e-8 absolute and
scaled-relative limits, maximum absolute difference 2.914433139267203e-09.
Mandatory regression, service and integration verification is in progress.

The independent references use alternate interpolation/sum formulations,
finite-frequency analytic response, unwrapped phase, direct DFT, chirp-Z,
permuted Cholesky covariance solves, direct convolution, explicit CFAR sums,
BFS grouping and bitmask truth matching. They import no production entrypoint
and consume no production results. Prior reference bytes and earlier module
files remain unchanged. Source stays at
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`.

P78 shorter apertures crop a retained full noise record. P79 sparse-aperture
recovery is dense reacquisition of the seeded scene. P80 assumes known geometry
and isolated range gates; phase RMSE removes the constant phase gauge. P81 uses
known translation alignment and small-angle cross-range. P84 controls compare
the retained first scan; its explicitly labeled eight-scan tracking sequence
uses the reviewed baseline Pfa/taper/correct replica. Scan 4 physically fades
the moving target before reception. Truth scores reports and does not drive
association. Requested Pfa is separate from empirical correlated-cell behavior.

Ledger: one distinct, seventy-five prior repairs, eight current, zero pending.
No further lesson batch is implied. Aggregate caliber, competency mapping and
cumulative-assessment review remain separate work under issue 441, with
whole-course numerical/curriculum/capstone maturity blocked. No MATLAB,
browser/accessibility, representative-learner, hardware or production claim.

Protected target merge requires separate owner approval. Hosted CI remains
nonmandatory under retained owner direction; all local gates remain mandatory.
Use bounded numerical-library threads and serialize heavy checks. Preserve
all runtime limits and source/history evidence; do not waive gates for load.
