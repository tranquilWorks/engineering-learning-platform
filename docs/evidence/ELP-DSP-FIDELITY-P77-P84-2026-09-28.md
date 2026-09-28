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
units in provenance, a retained value, source/artifact hashes and tolerances.

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
pass. All mandatory local gates completed successfully. Heavy checks ran
serially with numerical-library threads bounded to one and CPU affinity 9.
The complete backend command was exercised by both quick and full gates;
`./scripts/agent-verify.sh full` invoked `./scripts/verify.sh` with no skips.

| Local check | Result |
| --- | --- |
| New P77-P84 suite | 68 passed in 64.41 s, including all 188 offered control combinations |
| Focused DSP and caliber regression | 851 passed in 409.50 s |
| Contract | 72 passed in 75.39 s |
| Quick / complete backend | 1231 passed, 3 warnings in 964.72 s |
| Full / complete backend | 1231 passed, 3 warnings in 919.67 s |
| Frontend | Typecheck and production build passed under Node 22.12.0 |
| Deterministic catalog | Six courses, 290 modules, 290 interactive; pass |
| API protocol | Eight documents, 24 baseline/failure/recovery runs, eight stale-revision 422 rejections; exact recovery |
| Live TCP preview | Health, catalog, HTML, eight lesson documents and eight baseline runs passed |
| Scope and source | 137 allowed paths; exactly eight coverage digests; prior reference prefix and P01-P76 unchanged; source clean |
| Static checks | Scoped Ruff and Git diff checks passed |

The existing Starlette/httpx and FastAPI deprecation warnings and frontend
large-chunk warning do not change these passing results. The first live probe
preceded server readiness and returned connection refused; after health became
ready, all eight live document/run checks and the HTML route passed.

Reproduce the scoped checks through `contracts/verification.yaml`. The run used
`ELP_DSP_SOURCE_ROOT=courses/dsp-radar-learning`, `PYTHONPATH=apps/api/src`,
`PYTHONDONTWRITEBYTECODE=1` and numerical-library thread limits of one.
No test, runtime timeout, other course or workflow was changed to obtain a pass.

Local verification log identities:

| Gate | SHA-256 |
| --- | --- |
| focused | `7bbf39c5ed7cd11c32a90aa2d75d578e597faba58470f1c5215e7f7b01d48d97` |
| contract | `58415dd267441287cd9da6ff1ebce6dc98c6330a24b03d23448893e8c69e563d` |
| quick | `99bf10ec693c832f5a95d2441e187263647dd567225a43ba7551de3c5d684b9c` |
| full | `5e3fe9c304151594e679d413c8336768b237a274aad1f00c8e545268083a0c0d` |
| catalog | `e0ec19a3f9adf17cab941b6e63ba2fd0a89f5a0ca177b6997a4b612d0462e484` |
| http | `68690e2420a7fe36ce91a55e08924e3c16fe7080c4d1d750f7e4da1035929407` |
| scope | `5ed88c574ecac15536de25ddb716e6213e94592cd37ae9b8311372e05305be73` |

Control PR #523 local validation passed 252 root, 6 analog, 33 ELP and 15
Tranquility tests, plus schema, inventory and shell checks. Its hosted run
36434717867 failed with zero executed steps. Hosted CI remains nonmandatory
under retained owner direction; local gates are mandatory.

Implementation CI run [36438555341](https://github.com/tranquilWorks/engineering-learning-platform/actions/runs/36438555341)
for `83e53b1a1dcf49519782c596455128c7c25f23ae` completed frontend successfully.
Backend reported 66 failures / 1165 passes / 3 warnings in 550.43 seconds;
all failures were classified from the retained failure log: 64 missing pinned
source lesson files, one missing source-directory discovery check, and one
missing historical Git object used by the unchanged vehicle contract test.
The workflow checkout omits submodules and full history. Container validation
was skipped after backend failure. Failure-log SHA-256:
`e72b033700ec1a3bf540aa62a7807d0d27e3d7d8878b8fcce6481c2df1635197`.
No workflow, source test or runtime limit was weakened. This is a documented
hosted checkout limitation, not a claim of passing hosted backend/container CI.

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

## Review handoff

[PR #51](https://github.com/tranquilWorks/engineering-learning-platform/pull/51)
is ready for review, with implementation commit
`83e53b1a1dcf49519782c596455128c7c25f23ae`. The final documentation follow-up
changes only CURRENT_STATE, HANDOFF and this evidence file; tested production,
reference, fixture, contract and test files are unchanged. Protected merge has
not occurred and requires separate owner approval under the active batch.

Local preview:
http://127.0.0.1:8765/courses/dsp-radar/modules/77-focus-sar-with-backprojection

Final documentation updates may queue another nonmandatory hosted run; the
classified hosted result above is explicitly bound to the implementation head.
