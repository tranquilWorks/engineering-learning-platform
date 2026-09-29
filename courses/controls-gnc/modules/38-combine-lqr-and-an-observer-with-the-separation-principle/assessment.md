## P38 evidence task

Why does observer ratio leave the regulator abscissa unchanged but alter the plant trajectory? Which calculation establishes that K is LQR?

Before running: Increasing observer speed should change estimation-error decay but leave the regulator eigenvalues unchanged. Predict this before moving the ratio control.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Plant and estimate propagates actual coupled states from x=[1,0] and e=[0.1,0]. Actual observer error shows both normalized error components, not spectral envelopes. The window is 3/w seconds, so changing observer speed also changes its physical duration.

### Reasoning rubric

- Model: use `A=[[0,1],[0,0]], B=[0,1]^T, C=[1,0]` to explain the observed quantity rather than repeating a metric label.
- Evidence: The augmented block-triangular spectrum is the union of regulator and observer spectra. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode reverses the observer injection L. The error subsystem then has a positive pole, and its growing error drives the physical plant through BK e. Identify the measured consequence in your record.
- Recovery and scope: Restore the observer sign and reset controls. Verify both abscissae are negative and the CARE and separation residuals are near roundoff. State this limit: The finite demonstration excludes noise, saturation and model mismatch; arbitrarily fast observers are not certified here.

### Check your explanation

The off-diagonal BK block couples estimation error into the plant without changing the diagonal-block spectra. The CARE with the stated Q and R establishes the cost-derived gain; the small CARE residual verifies that calculation.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
