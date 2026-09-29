# DSP aggregate authored and software quality review

Status: implemented and mandatory local/browser/container verification passed;
verification completed `2026-09-29T01:00:56.526488+00:00`;
development merge tracked through [PR54](https://github.com/tranquilWorks/engineering-learning-platform/pull/54)
and CURRENT_STATE.

Exact predecessor PR53: `b107ac198543e8dfb563c6aae4175cc87da6210d`; tree `21028d29c7e5f139f6907c6fcf7f467d96bbbfe8`.
Exact merged control contract revision: `7b2e3c1e425b196b400856a714f699f2e225a83a`. Retained owner continuation
authorizes scoped verified development merge. No production action occurred.

## Delivered learner behavior

Every existing DSP lesson has a named Course checkpoint link and accessible
heading. Its authored task connects a concrete prediction, live controls/plots,
a dimensioned governing relation, expected reasoning and model boundary. It
preserves the lesson's exact named failure/recovery. Ten domain endpoints add
four concrete portfolio tasks and four rubric criteria, with links to real labs.
No score or completion is stored, and reading a rationale is not a learner pass.

The competency map covers all 84 existing identities with acyclic prerequisites,
84 formative assessments and ten cumulative assessments. Count is derived from
that graph; no modules were added. P84 integrates only its retained pulsed-radar
chain and fixed baseline eight-scan tracker. Separate branches receive separate
portfolios; selected first-scan controls do not recompute the tracking history.

The bounded P58 optimization adds execution headroom while preserving its
original lesson behavior and numerical evidence. It does not resolve or consume
any of the sixty other content findings.

Generic markdown navigation/rendering exposes named additional content without
DSP logic in the platform component. Per-lesson review disclosures carry the
assessment identifiers, retained comparison count and specific model limit.

## Numerical, identity and browser evidence

Fresh replay passed **417 independent comparisons**: two analytic P01 signatures
and five retained independent scenarios for each P02–P84. Expected vectors,
reference implementations and tolerances were unchanged. Five P01 analytic limits
cover signed frequency, phase/amplitude, aliasing and zero frequency. The retained
structural screen records 84 distinct normalized implementation shapes in
`dsp-structure-review.json`; structural distinctness alone is not fidelity proof. Ten cumulative
probes bind actual stage plots and dimensioned metrics. Existing source-fidelity,
physical-limit and failure tests remain enforced.

All source pins, DSP experiment.py, source lesson.md, numeric evidence and reference
oracles remain unchanged. All other course payloads are preserved from PR53 except the explicitly authorized
Robotics P58 execution fast path described below. Its complete returned outputs
are exactly preserved against the PR53 implementation.
Only assessment blocks/files are added to the DSP manifests. Actual CourseCatalog
input hashes and content digests reconcile conversion target identities and
coverage target digests; all other conversion/provenance fields are preserved.

| Verification | Actual result |
| --- | --- |
| `contract` | 103 passed in 88.43s (0:01:28) |
| `quick` | 1331 passed, 3 warnings in 1299.04s (0:21:39) |
| `full` | 1331 passed, 3 warnings in 1218.10s (0:20:18) |
| Independent numerical replay | 417 passed; 84 checkpoint content bindings; ten cumulative probes. |
| Frontend | Ten tests, typecheck and production build passed. |
| Focused real browser regressions | 16 passed. |
| Baked read-only nonroot HTTP | 290 modules passed. |
| Desktop/mobile delivery | 580 pages passed; zero serious/critical automated accessibility findings. |
| Assessment navigation | 168 checkpoint and 20 cumulative-block checks passed. |
| Actual interactions | 56 control/fault/recovery/reset sequences passed. |
| Content/screenshot reconciliation | 290 identities match both viewport rows; 56 sweep screenshots hash-checked. |

Final image: `sha256:53892d096feb4f23c30a7aa9fa2c2f0b25d7ebf3924be7e5d41f971672a39b67`. Local preview: `http://127.0.0.1:8771`.
`dsp-aggregate-review.json`, `browser-report.json`, `container-report.json` and
`dsp-assessment-visual-review.json` retain actual quantities, image identities,
screenshot hashes and the named visual-review sample. Automated navigation and
accessibility checks are distinct from manual screen-reader acceptance.

## Defects found and corrected during final verification

The first checkpoint browser test exposed a same-lesson fragment-navigation
reset. Native anchors recreated a route object, causing AppShell to refocus the
page and scroll to zero. Stable URL identity now preserves native anchor/history
behavior, while actual lesson changes retain focus/scroll reset. Control amendment
[PR540](https://github.com/tranquilWorks/portfolio-control/pull/540) authorized
this generic correction. The retained negative desktop/mobile replay is in
`dsp-navigation-observation.json`; the final regression covers keyboard jumps,
back/forward and next-lesson behavior, and all 168 checkpoint headings must
actually enter the viewport.

The existing conversion framework also rejected scientific JSON literals that
its YAML loader read as strings. Decimal-mantissa formatting restores compatible
numeric types without changing values or tolerances. Both loader and semantic
preservation checks now pass; all 417 comparisons were replayed after the final
content identities changed. See `dsp-metadata-observation.json`.

Control PR540 passed full local validation. Hosted run 36493135167 did not start
any steps because GitHub reported an account payment/spending-limit restriction.
No account or repository settings were changed. Target draft run 36493566921 passed frontend checks but failed 73 backend checks:
65 lacked pinned source checkout and eight lacked historical Git objects; its
container job was skipped. `dsp-hosted-ci.json` retains the exact failure rows.
Implementation-head run 36498067445 retained the same 73 failures plus fourteen
P58 preservation setup errors caused by the unavailable PR53 Git object; 1,244
tests and frontend checks passed. Target PR54 records the final-head hosted
status separately; no hosted pass is claimed.

Two full-gate attempts hit Robotics P58's unchanged three-second deadline at its
baseline controls. The first had 1,316 passing tests; the second failed during
catalog setup before a DSP assertion and was interrupted to retain its traceback.
The first overlapped quick; the second did not. Both observations are retained,
and neither establishes a scheduling cause.

Control [PR542](https://github.com/tranquilWorks/portfolio-control/pull/542)
authorized only a conservative already-feasible segment precheck in P58. It skips
scalar scans when all segment margins are safely positive; near-contact and
violating paths keep the original ordered correction. Objective, gradient,
1,200 iterations, endpoints, controls, numerical references/goldens and the
three-second limit remain unchanged. Complete outputs match PR53 exactly for
13 retained/corner cases; 72 projection edge cases also match. Fourteen focused
preservation tests passed. The highest observed before/after times were about
2.22/0.92 seconds in the measured sample. This is local timing evidence, not a
worst-case or concurrent-capacity guarantee. See `dsp-runtime-observation.json`.

A later quick attempt overlapping the browser sweep hit the unchanged DSP P26
default deadline during catalog setup; one failed fixture propagated 73 setup
errors. Five direct runs took 1.4–1.9 seconds, with similar wall and CPU time;
these observations do not prove the cause. No DSP model, reference, parameter or
timeout was changed. The failure is retained in the runtime observation.

After the browser sweep completed, mandatory contract, quick and full gates
ran sequentially without overlapping owned browser work. All container/browser
checks used the optimized image. The final results
are listed above. Control PR542 passed full local validation; hosted run
36497299277 did not start any steps because of the reported account payment/
spending-limit restriction. No settings or runtime-limit change was made.

## Remaining boundaries and rollback

DSP numerical, authored-curriculum and pulsed-capstone review passes only for the
stated synthetic software scope. Controls/Robotics/Vehicle retain all **60** known
findings and blocked aggregates. Nine source-only courses were not converted.
Learner effectiveness, manual screen-reader, audio playback, MATLAB, measured
hardware/vehicle/radar and production acceptance remain unperformed.

The container driver paces actual experiment requests one at a time; it neither
mocks results nor certifies concurrent-user capacity. The earlier two-CPU deadline
failure remains retained. Hosted CI is separately reported and nonmandatory under
owner direction; no green hosted claim is inferred from local results.

Rollback: revert this isolated assessment revision to the exact PR53 baseline.
No schema change, learner-data migration, source mutation or production deployment
is required. Historical item-conversion not_run claims remain intact as provenance;
current aggregate evidence is reported separately.
