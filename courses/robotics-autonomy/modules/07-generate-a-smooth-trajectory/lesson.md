# Generate a Smooth Trajectory

**Guiding question:** What inputs, observable effects, and failure modes matter when you generate a Smooth Trajectory?

## Concept and prediction

A time-normalized quintic polynomial connects rest-to-rest boundary conditions without velocity or acceleration jumps. Differentiating the same polynomial exposes actuator demand.

Before running the model, predict this: Increasing distance scales position, velocity, and acceleration; increasing duration reduces peak velocity as $1/T$ and acceleration as $1/T^2$. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$s(\tau)=10\tau^3-15\tau^4+6\tau^5$$ — The quintic progress variable satisfies position, velocity, and acceleration endpoint constraints.
- $$x=Ds,\quad\dot x=\frac{D}{T}s',\quad\ddot x=\frac{D}{T^2}s''$$ — Distance and duration scale the trajectory derivatives predictably.
- $$\tau=t/T\in[0,1]$$ — Normalized time keeps the shape independent of physical duration.

Symbols and units:

- $D$ — commanded travel distance (m); $T$ — move duration (s).
- $t$ — physical time (s); $\tau$ — dimensionless normalized time.
- $x,\dot x,\ddot x$ — position (m), velocity (m/s), and acceleration (m/s^2).
- $s',s''$ — derivatives with respect to normalized time.

Motion is one-dimensional in the positive x direction. Endpoint derivatives are evaluated from the analytic polynomial, not inferred from a coarse numerical difference.

## Manipulation: two one-variable sweeps

1. Sweep `distance_m` through [0.5,2,4] while holding the other controls at baseline. Check linear scaling of all dimensional outputs.
2. Restore baseline, then sweep `duration_s` through [1.5,4,8]. Check inverse-time scaling of peak velocity and acceleration.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent symbolic polynomial and endpoint-constraint evaluation; the actual vectors come from this Python experiment.

- At $t=0$, $x=\dot x=\ddot x=0$.
- At $t=T$, $x=D$ while velocity and acceleration return to zero.
- Doubling $T$ halves peak velocity and quarters peak acceleration.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Insufficient endpoint constraints.** The cubic smoothstep preserves zero endpoint velocity but has nonzero endpoint acceleration. A controller following it sees an acceleration jump at motion start and finish.

## Explanation and recovery

Disable the cubic profile and restore the quintic polynomial that enforces zero endpoint acceleration. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Differentiating with respect to normalized time and forgetting the $1/T$ factors.
- Calling a position-continuous profile smooth without checking its derivatives.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

