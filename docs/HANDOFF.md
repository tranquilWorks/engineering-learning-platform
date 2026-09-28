# Handoff

The owner approved merging PR #48 and the next twelve-lesson chunk on 2026-09-27.
PR #48 merged as `255427e3b3c6a31a66b74ad7f9836dad09b164e5`, tree
`3958e73ecf1914e4d2b5dee4a919c6b7275434f2`. Control PR #515 merged as
`549fd5867f2cd3b759a2af76e2a0be0350b8ee3c`; the active contract is an exact copy.

Branch: `codex/dsp-fidelity-p53-p64-20260927` in the isolated ELP worktree.
All twelve P53-P64 experiments, lessons and sixty independent comparisons are
implemented. Numerical replay passed at 1e-8 absolute/scaled-relative tolerance,
maximum absolute difference 2.0804691303055733e-11. All 240 control combinations
execute finite bounded output. Required broader verification remains in progress.

P53-P56 retain equations with private NumPy input streams; P57-P64 retain the
source private generator formulas and ordering. This is not MATLAB execution.
Prior modules and reference bytes are preserved; DSP source remains read-only at
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`. Ledger: one distinct, fifty-one prior
repairs, twelve current repairs, twenty pending. Whole-course maturity remains
blocked for P65-P84 and issue 441 remains open. Next proposed group is P65-P76,
after this batch's verification/merge and a new scoped contract.

Protected target merge requires separate approval; current approval covered #48.
Hosted source/history checkout prerequisites remain outside this contract and
hosted CI is nonmandatory by owner direction. All local gates remain mandatory.
Use `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` for serialized
verification, preserving the existing three-second runtime limits. Do not claim
browser/accessibility, learner, MATLAB runtime, hardware, deployment or production
validation. The current preview still serves the earlier process until refreshed.
