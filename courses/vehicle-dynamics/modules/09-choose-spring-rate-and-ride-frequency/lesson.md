# Derive Wheel Rate from Suspension Motion Ratio

Why does the suspension motion ratio enter wheel stiffness twice?

## Physical model

Define motion ratio r = spring displacement / wheel displacement. For an ideal lossless linkage, x_s = r x_w. Virtual work gives F_w dx_w = F_s dx_s, so F_w = r F_s. With F_s = k_s x_s, wheel force is F_w = k_s r² x_w, and wheel rate k_w = k_s r².

For a 300 kg corner mass, static wheel compression is x_static = mg/k_w and undamped ride frequency is f_n = √(k_w/m)/(2π). Wheel rate has units N/m; compression is in m and frequency is in Hz. The response plots wheel force against wheel displacement, with a horizontal corner-weight line at 2943 N. Their intersection represents the static equilibrium in this simplified corner model.

One ratio factor comes from displacement mapping and one from force mapping. Changing the definition of motion ratio would invert both factors, so the convention must be stated before using any remembered formula.

\[
k_w=k_s r^2,\qquad x_{\mathrm{static}}=\frac{mg}{k_w},\qquad f_n=\frac{1}{2\pi}\sqrt{\frac{k_w}{m}}.
\]

## Worked baseline

At k_s = 35000 N/m and r = 0.9, wheel rate is 28350 N/m. Static wheel compression is 2943/28350 ≈ 0.103810 m and ride frequency is about 1.547 Hz. Spring compression is 0.9 times the wheel compression. The spring's force is larger than wheel force by 1/r, which is consistent with virtual work rather than an unexplained force gain.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold r = 0.9 and increase spring rate from 15000 to 80000 N/m. Predict wheel rate proportional to spring rate, static compression inversely proportional to it, and frequency proportional to its square root. The primary sweep displays frequency, not stiffness.
2. Hold spring rate at 35000 N/m and vary r from 0.6 to 1.1. Predict frequency proportional to positive r, while wheel rate scales as r². Compare r = 0.6 with r = 0.9: the rate ratio is 2.25 and frequency ratio is 1.5.

## Named broken behavior

The toggle uses k_s r instead of k_s r², omitting the force-mapping factor. At r = 0.9 it predicts 31500 N/m and too little static compression. The virtual-work residual exposes the incorrect wheel rate even if the faulty rate is then used consistently in its own weight balance. At r = 1 the two formulas coincide and the fault is benign. For r above one the direction of its stiffness bias reverses.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

This single sprung corner assumes constant motion ratio, linear spring stiffness and no tire compliance, damping, preload, bump stop or unsprung mass. The undamped natural frequency is not a measured comfort score. The response window ends at 0.2 m; for some soft settings the static intersection lies outside that window, although the metric still reports the formal value. No suspension-travel limit is imposed by the model.

## Common mistakes

Do not substitute an inverse motion-ratio convention into this formula. Do not assume passing k_w x = mg validates the mapping from k_s to k_w; an incorrect stiffness can satisfy its own static balance.

## Formative checks

At fixed k_s = 35000 N/m, compare r = 0.6, 0.9 and 1.0. Derive wheel rate from displacement and force mapping, then calculate static compression and frequency ratios. Explain why r = 1 is an inadequate diagnostic for the single-factor fault.

Check your reasoning: Wheel rate uses two ratio factors and frequency uses one for positive r. The 0.6-to-0.9 rate ratio is 2.25; frequency ratio is 1.5. Unity hides the missing factor. A strong answer derives virtual work and checks both units and the chosen ratio convention.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
