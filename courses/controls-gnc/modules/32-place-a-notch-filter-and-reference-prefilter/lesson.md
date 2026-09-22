# Place a Notch Filter and Reference Prefilter

**Guiding question:** Why does suppressing a plant resonance require a different filter from shaping the command?

Tune a notch against a flexible mode and a prefilter against command bandwidth, then separate disturbance-loop and reference-path effects. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{N(s)=(s^2+2*zeta_z*w_n*s+w_n^2)/(s^2+2*zeta_p*w_n*s+w_n^2)}$$
$$\text{F(s)=w_f/(s+w_f)}$$
$$\text{reference map=F*T while disturbance map keeps N inside the loop}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The notch creates localized attenuation around its pole-zero frequency, while a unity-DC prefilter changes only the command path. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `prefilter_bandwidth_rad_s` at `4.0 rad/s` and sweep `notch_frequency_rad_s` from `5.0` through `12.0` to `20.0 rad/s`.
2. Restore `notch_frequency_rad_s` to `12.0 rad/s` and sweep `prefilter_bandwidth_rad_s` from `0.5` through `4.0` to `12.0 rad/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode moves the notch to half the selected frequency, leaving the actual flexible resonance exposed. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Align the notch with the measured resonance and tune the prefilter independently from command rise-time requirements. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- Both notch numerator and denominator have unity DC ratio.
- The first-order prefilter tends to zero at high frequency without changing disturbance rejection.

Teaching invariant: The notch creates localized attenuation around its pole-zero frequency, while a unity-DC prefilter changes only the command path.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `notch_frequency_rad_s` from sensitivity to `prefilter_bandwidth_rad_s`.
