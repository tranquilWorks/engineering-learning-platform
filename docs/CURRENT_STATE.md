# Current state

`ELP-GNC-MODELING-CLASSICAL-P25-P33` is the active issue-439 expansion batch. It starts from exact Engineering Learning Platform baseline `88e8f7407ce516a16e9397318c38902a78c11070` (tree `b713b922be3bc7a0c6fbe9f0b0bc5c485818b16c`) and latest Portfolio Control contract merge `66580fcd3764402d03d715ff09cee98ff74f5786`.

The reviewed competency map derives 68 total Controls/GNC modules from explicit outcomes, prerequisites, assessments, exclusions, cross-course handoffs, and three cumulative capstones. It retains the 24 source-bound modules and adds the smallest coherent set of 44 Python-first native lessons in seven batches sized 9, 9, 9, 5, 6, 3, and 3. The count is not a quota.

The first nine additions, P25-P33, implement operating-point linearization, realization and block equivalence, transient/system-type analysis, root locus, Nyquist, sensitivity loop shaping, lead/lag, notch/prefilter, and MIMO interaction/zeros/decoupling. Each has distinct governing equations, a complete lesson, two one-variable sweeps, named broken/recovery behavior, limiting cases, domain-specific axes and units, and separately retained independent and production signatures for five scenarios.

Controls/GNC now has 33 implemented interactive modules; the five-course catalog has 143 modules and 143 interactive modules. `curriculum_covered` and `capstone_integrated` remain `partial`, because P34-P68 and the cumulative capstones are not implemented. `learner_validated` remains `not_run`.

The immutable Controls/GNC source pin, P01-P24 source/conversion/fidelity records, DSP/Radar, Robotics, examples, generic platform behavior, dependencies, workflows, and deployment surfaces remain unchanged. No MATLAB runtime, browser/accessibility acceptance, learner study, physical hardware/HIL, certification, release, deployment, credentials/settings, or production validation is claimed.
