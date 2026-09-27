# Handoff

The owner approved PR #45 and continuing on 2026-09-27. Numerical replay repair
merged as `b7e684d595bd777602c9aa22cd489189efa6584b`, tree
`19a298703ab04794e855edffb8aa83a6f0e2ba83`. Control activation PR #503 merged at
`12ea755ee75f9fe7bc142f052362938d9cefb4c9`; the active contract is an exact copy.

Current branch: `codex/dsp-fidelity-p21-p28-20260927` in the isolated ELP worktree.
P21-P28 now have distinct source-specific algorithms, controls, plots, source
lessons, five independent expected/actual scenarios, and failure/recovery checks.
All mandatory local gates passed at implementation commit
`152ddf6ad3e534f7b4ed11e9f73b9d909a7d60a5`: 405 focused DSP checks, 72 contract
checks, quick and full (785 tests each), schema/catalog, lint, frontend typecheck
and build, scope/source audit, and API/live HTTP smoke checks. The final follow-up
commit updates evidence and status documents only. P01-P20 and P29-P84 module
bytes remain unchanged.

Review: https://github.com/tranquilWorks/engineering-learning-platform/pull/46
Local preview: http://127.0.0.1:8765/courses/dsp-radar/modules/21-visualize-am-as-carrier-and-sidebands
Evidence: `docs/evidence/ELP-DSP-FIDELITY-P21-P28-2026-09-27.md`.
PR #46 is prepared for review; merge remains pending owner approval.

The implementation covers AM/FM, BPSK/QPSK, RRC and matched filtering, multipath
ZF/regularized inversion, eight-tap LMS, independent BPSK Monte Carlo trials and
ROC/amplitude-estimator limits. Read-only source pin:
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`. No MATLAB runtime parity is claimed.

Issue 441 stays open. Catalog remains 6 courses / 290 modules / 290 interactive.
The ledger distinguishes one already-distinct, nineteen prior repairs, eight
current repairs and fifty-six pending. P29 is the next source item after this
batch. Course numerical/curriculum/capstone maturity remains blocked.

Hosted setup debt is separate: PR #46 implementation run 36293155510 had
775 passes and ten failures (nine DSP source checks and one historical vehicle
commit check) from missing submodule/history in the checkout; frontend passed.
The complete local suite passed all 785 checks, retaining these gates.
No workflow/vehicle framework modification is authorized by the DSP contract.

Protected target merge retains a separate human authorization requirement.
The owner's present merge approval applied to PR #45. No browser/accessibility,
learner, hardware, release/deployment, credentials or production claim is made.
