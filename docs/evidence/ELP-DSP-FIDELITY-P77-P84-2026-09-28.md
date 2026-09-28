# Final DSP/Radar item fidelity group P77-P84

The owner requested the final group after the PR #50 merge/continuation handoff.
PR #50 merged as `f05403ef2c0a5e31d7045c0cb796b2e136ca50c9`, tree
`f30d2a4a74d1fb76b94c6446095698615847cbbb`. Control PR #523 merged as
`d0c6bc74992a1e62aa6f372334be5f7a079a20ec`; the active contract matches its
approved batch file exactly. This change repairs eight existing lessons.

## Implemented evidence chains

| Item | Processing and learner failure | Independent formulation |
| --- | --- | --- |
| P77 | Complex row interpolation, path phase, pixel sums; 10 mm path error | Coordinate interpolation and row-vector pixel sums |
| P78 | Signed migration correction, coherent profiles, fixed/following images; wrong interpolation sign | Independent coordinate resampling and direct pixel sum |
| P79 | Frequency and aperture responses, Hamming and sampling sweeps; sparse grating responses | Analytic finite-frequency response and rationalized path differences |
| P80 | Source phase screen, isolated-gate phase-gradient correction; contaminated reference | Unwrapped deramped phase and independently summed focus |
| P81 | Rotating scatterer histories, translation alignment, range/angle transforms; omitted alignment | Direct range and angle DFT matrices |
| P82 | Separate reference/surveillance, least-squares cancellation, delay/Doppler ambiguity; partial cancellation | Least-squares solver and chirp-Z ambiguity transform |
| P83 | Guarded training, loaded covariance, normalized adaptive map; contaminated training | Sensor-major permutation, Cholesky solves and component SCNR |
| P84 | Waveform, echoes, receiver inverse, compression, Doppler, CFAR, reports and gated track; wrong replica | Direct convolution/DFT, explicit CFAR stencil, BFS, bitmask matching and independent track recurrence |

Every lesson preserves its pinned source text and guiding question, offers two
physical controls, prediction, one-variable manipulations, equations with units,
intermediate plots, a named failure, recovery and focused teach-back. Full arrays
drive computation before display decimation. Every expected/actual field has
units in provenance, a retained value, input/source hashes and tolerances.

Forty baseline/two-sweep/broken/recovery comparisons pass both 1e-8 absolute
and scaled-relative limits. Maximum absolute difference:
`2.914433139267203e-09`. The reference imports no production entrypoint and
consumes no production outputs. The prior 185460 bytes retain SHA-256
`41ad296232898f8d5b353261df02064ed52ad6d9c1d757e93703868455c6b9fd`.

Private input formulas preserve the source generators and column-major order.
P78 aperture controls crop a full retained noise record. P79 dense recovery is
reacquisition, not inversion of missing sparse samples. P80 assumes known
geometry and isolated reference gates; phase scoring removes a constant gauge.
P81 assumes known translation and small-angle cross-range. P84 controls compare
the retained first scan; the eight-scan track is explicitly fixed to the source
baseline configuration. The scan-4 fade enters before reception and causes a
physical coast. Truth is confined to offline scoring. Empirical false-cell rate
is distinct from requested homogeneous-cell Pfa.

## Validation state

Independent retained comparisons: passed, 40/40. Scope/source inspection passed:
only P77-P84 coverage digests change, earlier module files and reference prefix
are preserved, source is clean at `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`,
and the active contract is the exact merged control. Scoped Ruff and diff checks
pass. Mandatory regression and service gates are in progress; no completion
claim is made for gates still running.

Control PR #523 local validation passed 252 root, 6 analog, 33 ELP and 15
Tranquility tests, plus schema, inventory and shell checks. Its hosted run
36434717867 failed with zero executed steps. Hosted CI remains nonmandatory
under retained owner direction; local gates are mandatory.

## Exit ledger and claim boundary

One distinct + seventy-five prior repairs + eight current repairs + zero
pending = 84 existing items. Catalog inventory remains six courses, 290 modules
and 290 interactive modules. Item repairs are complete; aggregate caliber,
competency mapping and cumulative-assessment review remain separate work.
Whole-course numerical/curriculum/capstone maturity remains blocked and issue
441 stays open. No further lesson batch is automatically authorized.

Evidence is deterministic software and protocol evidence only. No MATLAB runtime,
browser/accessibility, representative-learner, hardware/HIL, certification,
deployment or production claim. Protected target merge retains separate owner
approval. Rollback is a revert of this isolated batch to the merged PR #50
baseline; no schema, dependency, source or runtime migration is needed.
