# Current state

`ELP-GNC-FIDELITY-P01-P24` is the active remediation batch. It starts from
exact Engineering Learning Platform baseline
`1506591946ec8e96fe3201e8893b8ad851a1685a` (tree
`cff72df08f1c37655e912ca1c24f90e27222f6e3`) and Portfolio Control merge
`0038f6ed725ae2fc7b3eb6647e9621a2ad23db34`.

Controls/GNC retains the immutable source pin
`ffd6623ee2cf8ccd8599fffd935ef07370750fa3` and the exact P01-P24 inventory.
Each item now has a closed semantic map, domain-specific plot axes, explicit
source omissions, and independently generated baseline, two one-variable
sweeps, broken, and recovery evidence. P01's source failure convention and
P24's two-way packet/event order were repaired. P20 is described narrowly as
a two-fixed-gain comparison; it does not claim general robust synthesis.

The course-caliber projection now records Controls/GNC as `source_authored:
passed`, `platform_converted: passed`, and `numerically_verified: passed` at a
deterministic software-only boundary. `curriculum_covered` and
`capstone_integrated` remain `partial`; `learner_validated` remains `not_run`.
Issue #439 is the sole owner of Controls/GNC competency mapping and expansion.

The catalog remains five courses, 134 modules, and 134 interactive modules.
Those counts are implementation inventory, not curriculum completeness.
DSP/Radar issue #441 and Robotics issue #440 remain untouched. Vehicle
Dynamics remains queued and unimplemented under its existing hold.

No licensed MATLAB runtime, browser/accessibility acceptance, learner study,
physical hardware/HIL, bench, field, release, deployment, credentials/settings,
or production validation is claimed.
