# Control Contact with Impedance

**Guiding question:** What inputs, observable effects, and failure modes matter when you control Contact with Impedance?

## Concept and prediction

Impedance control commands a spring-damper relationship instead of a rigid position. In contact, the controller spring and wall compliance share the requested displacement.

Before running the model, predict this: Higher virtual stiffness raises contact force and moves penetration toward the command; damping mainly changes the transient. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$m\ddot x=K(x_d-x)-B\dot x-F_c$$ — Virtual spring and damper drive penetration while contact force opposes it.
- $$F_c=K_e\max(x,0)$$ — A unilateral linear wall produces force only during positive penetration.
- $$x_{ss}=\frac{K}{K+K_e}x_d$$ — Static controller and environment forces balance.

Symbols and units:

- $x,x_d$ — actual and desired wall penetration (m; control displayed in mm).
- $m$ — effective endpoint mass (kg).
- $K,B$ — virtual stiffness (N/m) and damping (N s/m).
- $K_e$ — environment stiffness (N/m); $F_c$ — contact force (N).

Positive x points into the wall. Contact force magnitude is reported positive, but its signed contribution to the dynamics is negative (opposes penetration).

## Manipulation: two one-variable sweeps

1. Sweep `stiffness_n_m` through [75,200,600] while holding the other controls at baseline. Compare steady penetration and force sharing with the wall.
2. Restore baseline, then sweep `damping_ns_m` through [4,20,60]. Compare overshoot and settling without changing the static balance.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent independent linear-system equilibrium and separately formulated state recurrence; the actual vectors come from this Python experiment.

- With $x_d=0$ and zero initial state, force and motion remain zero.
- At static balance, $K(x_d-x)=K_e x$.
- Increasing damping changes settling but not the ideal static penetration.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Disconnected wall reaction.** The broken model removes $F_c$ from the dynamics and reports zero contact force even while commanding penetration into the wall. It violates the action-reaction path.

## Explanation and recovery

Disable the disconnected-contact mode so the wall reaction opposes penetration in the dynamics and force diagnostic. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Using the contact-force magnitude with the wrong sign in the motion equation.
- Interpreting large controller stiffness as proof of safe physical contact.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

