# Current state

`ELP-DSP-FIDELITY-P02-P10` is the first incremental repair batch for issue 441. It starts from exact target baseline `4b613a79bfe3cbd997e64e8372a58956533dae2c` (tree `9d7de9eb1399cdc541cc8475a2bc0a380c9c00e5`) and final Portfolio Control authorization `67620c1580976fda9047d9706cde9a34500ee82e`.

DSP/Radar P02-P10 now use nine distinct source-faithful bounded NumPy experiments. They cover sampling measurements, alias folding, quantization, noise families, impulse responses, convolution, correlation, FIR/IIR behavior, and multirate artifacts. Each retains baseline, two one-variable sweeps, a named broken case, exact recovery, and five independently formulated evidence scenarios. Generic controls and shared `PHASE` dispatch are absent from the repaired items, and normalized AST checks prevent an unexplained identical implementation shape.

The remediation ledger is deliberately incremental: P01 is the prior distinct conversion, P02-P10 are repaired, and P11-P84 remain pending. DSP/Radar therefore stays blocked at `numerically_verified`, `curriculum_covered`, and `capstone_integrated`; issue 441 remains open. The catalog remains six courses, 290 modules, and 290 interactive experiments.

MATLAB runtime comparison, audio playback, browser/accessibility validation, representative learner validation, physical HIL/hardware, certification, release, deployment, credentials/settings, and production validation remain explicitly unperformed.
