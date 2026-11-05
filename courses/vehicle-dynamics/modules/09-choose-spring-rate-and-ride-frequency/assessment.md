# P09 course checkpoint

## Predict and derive

Use virtual work and spring energy to derive the squared motion-ratio law.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Unit-displacement virtual work`

## Controlled comparison

- `spring_rate_n_m`: 35000.0 → 15000.0. Hold the other controls at baseline; predict and explain the change before executing.
- `motion_ratio`: 0.9 → 1.1. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

With motion ratio defined as spring travel divided by wheel travel, spring displacement is r*z. Energy is k_s*(r*z)²/2, so wheel rate is k_s*r². At r=0.9 and k_s=35000 N/m, wheel rate is 28350 N/m. Using r instead of r² violates energy equivalence even if units still look correct. Explicitly distinguish this convention from the reciprocal convention used in some suspension references.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Constant motion ratio excludes travel-dependent geometry, installation preload and nonlinear bump stops.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P09 evidence task

At fixed k_s = 35000 N/m, compare r = 0.6, 0.9 and 1.0. Derive wheel rate from displacement and force mapping, then calculate static compression and frequency ratios. Explain why r = 1 is an inadequate diagnostic for the single-factor fault.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Wheel rate uses two ratio factors and frequency uses one for positive r. The 0.6-to-0.9 rate ratio is 2.25; frequency ratio is 1.5. Unity hides the missing factor. A strong answer derives virtual work and checks both units and the chosen ratio convention.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At k_s = 35000 N/m and r = 0.9, wheel rate is 28350 N/m. Static wheel compression is 2943/28350 ≈ 0.103810 m and ride frequency is about 1.547 Hz. Spring compression is 0.9 times the wheel compression. The spring's force is larger than wheel force by 1/r, which is consistent with virtual work rather than an unexplained force gain.

Do not substitute an inverse motion-ratio convention into this formula. Do not assume passing k_w x = mg validates the mapping from k_s to k_w; an incorrect stiffness can satisfy its own static balance.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
