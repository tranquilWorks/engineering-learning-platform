# Handoff

Issue #439 now has a reviewed competency-derived 68-module Controls/GNC plan and its first implementation batch, P25-P33. The authoritative artifacts are:

1. `courses/controls-gnc/competency-map.yaml` — learners, outcomes, prerequisites, 24 competency areas, 68 lesson identities, assessments, exclusions, handoffs, batch derivation, and three capstones.
2. `courses/controls-gnc/expansion-map.yaml` and each native module's `design.yaml` — implemented native identity, governing equations, five scenarios, signature fields/units, limiting cases, teaching invariant, tolerance, and claim boundary.
3. `courses/controls-gnc/expansion_reference_cases.py` — independent analytic/numerical signatures that import no production experiment, consume no production result, and perturb no production value.
4. Each module's `expected-independent.json` and `actual-production.json` — separately generated baseline, two sweep, broken, and recovery vectors.
5. `docs/evidence/ELP-GNC-MODELING-CLASSICAL-P25-P33-2026-09-22.md` — retained first-batch verification and limitations.

The next authorized work must use a new exact-baseline Portfolio Control contract for P34-P42. Do not modify P01-P33 while adding that batch. The remaining sequence is P34-P42 state/digital, P43-P51 nonlinear/robust/system-ID, P52-P56 estimation, P57-P62 navigation, P63-P65 guidance, and P66-P68 cumulative capstones.

Issue #439 stays open until all seven batches merge and cumulative verification passes. No native lesson claims MATLAB/source equivalence. Browser/accessibility, learner effectiveness, physical hardware/HIL, certification, release, deployment, credentials/settings, and production validation remain unperformed.
