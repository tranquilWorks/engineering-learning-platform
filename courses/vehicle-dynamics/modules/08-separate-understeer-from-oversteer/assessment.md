# P08 course checkpoint

## Predict and derive

Classify understeer, neutral steer and oversteer before interpreting a characteristic or critical speed.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Static axle weights divided by stiffness; critical boundary and stable mask`

## Controlled comparison

- `front_cornering_stiffness_n_rad`: 90000.0 → 45000.0. Hold the other controls at baseline; predict and explain the change before executing.
- `rear_cornering_stiffness_n_rad`: 100000.0 → 140000.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For K=Wf/Cf-Wr/Cr, steer demand is L/R+K*a_y/g. Positive K gives characteristic speed sqrt(g*L/K); negative K gives a distinct critical speed sqrt(-g*L/K). Neutral steer has neither finite speed. Near K=0 the relevant speed diverges; a zero placeholder means unavailable, not stationary instability. Vary front and rear stiffness separately to establish their opposite contributions.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The critical-speed singularity belongs to the linear steady model and is not a safe-speed recommendation.

Competency links: VD-HANDLING-LINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P08 evidence task

Use the sliders to select understeer and oversteer pairs, then derive a neutral pair algebraically within the allowed stiffness ranges. The slider steps do not generally reach exact neutral steer: report that boundary as a calculated case rather than claiming you selected it. For each case, report K, critical-speed availability and the steering trend with speed. At a fixed non-neutral pair compare nominal and omission at 25 m/s, then explain why the fault is invisible at neutral.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

The sign of K classifies the three setups; only negative K outside the numerical neutral band yields a finite critical speed. Neutral satisfies l_r/C_f = l_f/C_r. The omission removes K a_y from steer and K V² from the denominator. Full reasoning separates formal algebra, stable operation and unavailable metrics.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

With C_f = 90000 and C_r = 100000 N/rad, K = 0.00219715 s²/m and the gradient is about 1.23495 deg/g. At 25 m/s the denominator is 3.94322 m. For a_y = 1 m/s², δ ≈ 0.36149°. There is no oversteer critical speed for this positive K. Neutral steer occurs when C_f/C_r = l_r/l_f ≈ 1.23478, rather than when the two stiffnesses are simply equal.

A displayed internal zero sentinel is not a physical critical speed. Equal axle stiffness is not generally neutral steer, because lever arms and static axle loads differ. Removing K from an equation does not remove the underlying vehicle compliance.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
