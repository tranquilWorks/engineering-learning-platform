# Combine LQR and an Observer with the Separation Principle

Separation combines an optimal state-feedback regulator with an independently designed observer. Positions, velocities and input are normalized using one metre, one second and one m/s²; the CARE uses these normalized coordinates and time. The bandwidth setting b parameterizes the cost rather than prescribing two real poles.

## Model and equations

\[
A^T P+PA-PBR^{-1}B^TP+Q=0,\qquad K=R^{-1}B^TP
\]

`A=[[0,1],[0,0]], B=[0,1]^T, C=[1,0]`

`A^T P+P A-P B B^T P+Q=0; K=B^T P; Q=diag(b^4,b^2), R=1`

`e_dot=(A-LC)e; x_dot=(A-BK)x+BK e; L=[3w,2w^2]^T`

Worked example: For b=1.5, Q=diag(5.0625,2.25), and the double-integrator CARE gives K=[2.25,2.598076]. The regulator poles have real part −1.299038/s. With ratio 3, w=4.5/s and observer poles are −4.5 and −9/s.

## Baseline workflow

Increasing observer speed should change estimation-error decay but leave the regulator eigenvalues unchanged. Predict this before moving the ratio control.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Plant and estimate propagates actual coupled states from x=[1,0] and e=[0.1,0]. Actual observer error shows both normalized error components, not spectral envelopes. The window is 3/w seconds, so changing observer speed also changes its physical duration.

## Two one-variable sweeps

Increase regulator bandwidth from 1.5 to 4/s: inspect the changed cost-derived K and regulator abscissa. Reset, then raise observer speed ratio from 3 to 8: the observer abscissa moves while the regulator abscissa stays fixed.

## Intentionally broken case

Broken mode reverses the observer injection L. The error subsystem then has a positive pole, and its growing error drives the physical plant through BK e.

## Recovery

Restore the observer sign and reset controls. Verify both abscissae are negative and the CARE and separation residuals are near roundoff.

## Limiting cases and invariants

- The augmented block-triangular spectrum is the union of regulator and observer spectra.
- With zero initial estimation error, the observer-error state stays zero.
- The finite demonstration excludes noise, saturation and model mismatch; arbitrarily fast observers are not certified here.

## Independent evidence

Closed-form double-integrator CARE gains and the observer characteristic polynomial independently determine abscissae. Tests verify the Riccati identity and every sampled augmented-state transition. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

A gain chosen by pole placement is not LQR unless it is derived from a declared cost. Negative eigenvalues alone do not make a plotted envelope an actual state trajectory.

## Teach-back

Why does observer ratio leave the regulator abscissa unchanged but alter the plant trajectory? Which calculation establishes that K is LQR?

Answer rationale: The off-diagonal BK block couples estimation error into the plant without changing the diagonal-block spectra. The CARE with the stated Q and R establishes the cost-derived gain; the small CARE residual verifies that calculation.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
