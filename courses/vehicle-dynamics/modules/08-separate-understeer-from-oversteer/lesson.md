# Interpret Understeer and Critical-Speed Boundaries

When is a critical speed meaningful, and what does a formal curve beyond it mean?

## Physical model

For m = 1320 kg, L = 2.57 m, l_f = 1.15 m and l_r = 1.42 m, define K = (m/L)(l_r/C_f − l_f/C_r), in s²/m. The controls vary positive front and rear cornering stiffness in N/rad. The steer gradient is K g converted from radians to degrees, in deg/g.

For specified lateral acceleration a_y, the steady relation is δ = (L/V² + K)a_y. The response uses a_y = 1 m/s² and plots road-wheel steer in degrees against speed. Positive K is understeer; zero is neutral steer; negative K is oversteer. For K < 0 the denominator L + KV² reaches zero at V_crit = √(−L/K).

At and beyond that oversteer boundary the formal steady algebra is not a stable operating prediction. The chart distinguishes that branch. A critical speed is unavailable for understeer or neutral steer; the metric says **Unavailable**, not a physical speed of zero. Numerical classification treats |K| within 1e−14 s²/m as neutral for critical-speed availability. The actual K is retained in the steering relation.

\[
K=\frac{m}{L}\left(\frac{l_r}{C_f}-\frac{l_f}{C_r}\right),\qquad \delta=\left(\frac{L}{V^2}+K\right)a_y.
\]

## Worked baseline

With C_f = 90000 and C_r = 100000 N/rad, K = 0.00219715 s²/m and the gradient is about 1.23495 deg/g. At 25 m/s the denominator is 3.94322 m. For a_y = 1 m/s², δ ≈ 0.36149°. There is no oversteer critical speed for this positive K. Neutral steer occurs when C_f/C_r = l_r/l_f ≈ 1.23478, rather than when the two stiffnesses are simply equal.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold C_r = 100000 N/rad and vary C_f from 45000 to 140000 N/rad. Predict decreasing K as the front becomes stiffer. Cross neutral near C_f = 123478.26 N/rad and identify where a finite critical speed becomes available.
2. Hold C_f = 90000 N/rad and vary C_r over the same range. Predict increasing K as rear stiffness rises. Inspect the speed-response chart at an oversteer selection, distinguishing the stable branch from its formal continuation. Do not infer a safe operating speed solely from this instructional boundary.

## Named broken behavior

The fault omits K from the steering demand and uses δ = La_y/V². It preserves the stiffness-derived K and critical-speed metrics so the missing contribution can be identified rather than concealed. At the defaults and 25 m/s, omission reduces demand to about 0.23560°. The compliance residual in the selected 25 m/s denominator is −K·625. A truly neutral setup makes this omission benign. The fault is not evidence that changing tire stiffness removed the physical stability boundary.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The interpretation assumes the same linear bicycle geometry and constitutive laws used in deriving K. It excludes transient control, tire-force limits and nonlinear stabilization. The plotted inverse relation δ for fixed a_y remains finite at V_crit; the forward response a_y for fixed nonzero δ is singular there. Do not confuse those two experiments. Formal negative steering demand beyond the critical boundary is not a prediction that the vehicle will stably turn opposite its steer.

## Common mistakes

A displayed internal zero sentinel is not a physical critical speed. Equal axle stiffness is not generally neutral steer, because lever arms and static axle loads differ. Removing K from an equation does not remove the underlying vehicle compliance.

## Formative checks

Use the sliders to select understeer and oversteer pairs, then derive a neutral pair algebraically within the allowed stiffness ranges. The slider steps do not generally reach exact neutral steer: report that boundary as a calculated case rather than claiming you selected it. For each case, report K, critical-speed availability and the steering trend with speed. At a fixed non-neutral pair compare nominal and omission at 25 m/s, then explain why the fault is invisible at neutral.

Check your reasoning: The sign of K classifies the three setups; only negative K outside the numerical neutral band yields a finite critical speed. Neutral satisfies l_r/C_f = l_f/C_r. The omission removes K a_y from steer and K V² from the denominator. Full reasoning separates formal algebra, stable operation and unavailable metrics.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
