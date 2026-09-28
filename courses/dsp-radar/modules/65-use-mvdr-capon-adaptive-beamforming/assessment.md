### DSP-F65 · Defend an array estimate under mismatch

**Competency DSP-C65:** Eight half-wavelength sensors observe a weak 3-degree source and a 25 dB interferer at 30 degrees. R=X X^H/N; loading is alpha trace(R)/8; w=solve(R+delta I,a)/(a^H solve). Components use the true manifold only for performance accounting.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter); [P63 — Implement Conventional Delay-and-Sum Beamforming](/courses/dsp-radar/modules/63-implement-conventional-delay-and-sum-beamforming).

**Predict and investigate.** Compare snapshots=4 and 128, then increase loading_alpha. Use eigenvalues, pattern and components to explain the robustness/interference-rejection tradeoff.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named four-snapshot covariance is singular without loading. A barely loaded 6-degree look can suppress the true 3-degree source.
- Recover: On the unchanged four snapshots, alpha=.1 stabilizes the solve; correcting the look restores unit true response. Disable the toggle to restore the selected baseline.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `w=R_loaded^-1 a/(a^H R_loaded^-1 a)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Limited snapshots make covariance poorly supported or rank deficient. Trace-scaled loading regularizes inversion. The distortionless constraint protects the assumed steering vector, so mismatch can still suppress the actual desired signal.

**Limit the claim.** A small constraint residual is necessary but does not prove high output SINR or correct steering.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
