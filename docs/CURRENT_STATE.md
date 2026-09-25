# Current state

`ELP-DSP-FIDELITY-P11-P20` is the second incremental repair batch for issue 441. It starts from exact target baseline `a24818f42ff267394ee4ec97727ddb7d1978e3f4` (tree `1b5f62cc0adaa1796c459e7def317405cea4fe37`) and merged Portfolio Control authorization `8306551de3f32f9cb15c38efb3f5ab1e886756f0`.

DSP/Radar P11-P20 now use ten distinct source-faithful bounded NumPy experiments. They cover FFT-bin mapping, leakage and windows, zero padding versus true resolution, periodogram/Welch PSD, STFT tradeoffs, analytic signals, complex downconversion, real versus complex sampling, I/Q impairment correction, and noisy tone estimation. Each retains baseline, two one-variable sweeps, a named broken case, exact recovery, and five independently formulated evidence scenarios. Generic controls and shared `PHASE` dispatch are absent from P02-P20, and normalized AST checks prevent unexplained identical implementation shapes across that repaired range.

The remediation ledger is deliberately incremental: P01 is the prior distinct conversion, P02-P10 are prior-batch repairs, P11-P20 are current-batch repairs, and P21-P84 remain pending. DSP/Radar therefore stays blocked at `numerically_verified`, `curriculum_covered`, and `capstone_integrated`; issue 441 remains open. The catalog remains six courses, 290 modules, and 290 interactive experiments.

MATLAB runtime comparison, audio playback, browser/accessibility validation, representative learner validation, physical HIL/hardware, certification, release, deployment, credentials/settings, and production validation remain explicitly unperformed.
