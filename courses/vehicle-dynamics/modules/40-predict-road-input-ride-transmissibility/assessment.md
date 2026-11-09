# P40 course checkpoint

## Predict and derive

Translate a spatial road wavelength into excitation frequency and derive absolute body transmissibility.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `f=v/lambda_road`
- `H=(k+j c omega)/(k-m omega^2+j c omega)`
- `a_body=|H| z_road omega^2`

## Controlled comparison

- `speed_m_s`: 22 → 35. Hold the other controls at baseline; predict and explain the change before executing.
- `road_wavelength_m`: 8 → 16. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Road frequency is f=v/lambda and omega=2*pi*f. At 22 m/s over an 8 m wavelength, f=2.75 Hz and omega is about 17.2788 rad/s. For base excitation, H=(k+j*c*omega)/(k-m*omega²+j*c*omega); omitting the numerator's damper term changes the physical forcing. Body acceleration amplitude is omega²*abs(H)*road amplitude. Very slow excitation gives displacement ratio near one, not zero.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This sprung-mass SDOF model excludes wheel-hop dynamics and tire contact; it does not establish a ride-comfort standard.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
