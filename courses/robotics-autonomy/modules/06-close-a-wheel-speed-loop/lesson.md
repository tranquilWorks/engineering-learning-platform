# Close a Wheel-Speed Loop

**Guiding question:** What inputs, observable effects, and failure modes matter when you close a Wheel-Speed Loop?

## Concept and prediction

A PI controller commands motor voltage from speed error. The plant and controller are sampled, and the actuator clips voltage, so discrete-time scaling and anti-windup are part of the model—not implementation details.

Before running the model, predict this: Proportional gain speeds the first correction; integral gain removes residual error but can accumulate badly during saturation. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$e_k=\omega_c-\omega_k,\quad u_k=K_p e_k+K_i I_k$$ — PI feedback combines present and accumulated error.
- $$I_{k+1}=I_k+T_s e_k$$ — The integral state has units of radians and must include sample time.
- $$\omega_{k+1}=\omega_k+\frac{T_s}{\tau}(K u_{sat,k}-\omega_k)$$ — A first-order wheel plant responds to saturated voltage.

Symbols and units:

- $\omega_c,\omega$ — commanded and measured wheel speed (rad/s).
- $K_p$ — proportional gain (V/(rad/s)); $K_i$ — integral gain (V/rad).
- $I$ — accumulated angular error (rad); $T_s$ — sample interval (s).
- $u_{sat}$ — voltage after actuator saturation (V); $\tau$ — plant time constant (s).

Positive voltage produces positive wheel speed. Error is command minus measurement. Conditional integration freezes the integrator only when saturation and error would push farther into saturation.

## Manipulation: two one-variable sweeps

1. Sweep `kp_v_per_rad_s` through [0.5,1.5,3.5] while holding the other controls at baseline. Compare rise time and proportional effort before changing integral action.
2. Restore baseline, then sweep `ki_v_per_rad` through [0.5,4,10]. Compare steady error, overshoot, and saturation duration.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent separately formulated discrete recurrence with explicit saturation logic; the actual vectors come from this Python experiment.

- With $K_i=0$, proportional control can leave a steady error.
- With command zero and zero initial state, every state remains zero.
- Removing voltage saturation should make anti-windup inactive.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Unscaled discrete integrator.** The broken controller adds $e_k$ instead of $T_s e_k$. Its effective integral gain is one hundred times larger at the 10 ms sample time, producing saturation and windup.

## Explanation and recovery

Disable the unscaled integrator so error is accumulated as error times sample interval and saturation can pause harmful windup. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Using continuous-time integral gain in a recurrence without multiplying by sample time.
- Judging tracking without also looking at voltage saturation and integral state.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

