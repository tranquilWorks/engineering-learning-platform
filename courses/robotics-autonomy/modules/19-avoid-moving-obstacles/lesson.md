# Avoid Moving Obstacles

**Guiding question:** What inputs, observable effects, and failure modes matter when you avoid Moving Obstacles?

## Concept and prediction

Dynamic collision avoidance asks whether two moving bodies violate separation at the same future time. Current distance and static-map clearance are insufficient; relative velocity determines closest point of approach.

The default obstacle starts at $(5,-5)$ m and crosses upward while the robot moves generally toward +x. Predict the collision time for a straight robot heading and which turn direction gives the smallest safe deviation.

## Model, symbols, and equations

- $$\mathbf r(t)=\mathbf r_0+(\mathbf v_o-\mathbf v_r)t$$ — relative position.
- $$t_{\mathrm{CPA}}=\operatorname{clip}\left(-\frac{\mathbf r_0^T\mathbf v_{rel}}{\|\mathbf v_{rel}\|^2},0,T\right)$$ — closest-approach time over horizon $T$.
- $$d_{\mathrm{CPA}}=\|\mathbf r(t_{\mathrm{CPA}})\|$$ — predicted minimum separation.

World +x is the robot's nominal goal direction, +y is left, velocities use m/s, position and separation use metres, time uses seconds, and positive heading is counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `obstacle_speed_m_s` through [0.2,1,2]. The crossing time moves relative to the robot's arrival and can create or remove conflict.
2. Restore baseline, then sweep `prediction_horizon_s` through [2,8,10]. A short horizon may not see the future crossing soon enough.

The encounter plot shows actual trajectories. The candidate plot shows predicted closest separation versus robot heading and the required safety threshold.

## Evidence and limiting cases

An independent scalar loop enumerates heading candidates and analytically evaluates closest approach. Production uses a vectorized candidate calculation, then simulates actual trajectories.

- With zero relative velocity, separation remains constant.
- A horizon shorter than the collision time cannot reject that future conflict.
- Large current distance does not imply safety when relative motion closes it.

This is constant-velocity software prediction, not a full dynamics, perception, physical robot, HIL, or field result.

## Intentionally broken assumption

**Moving obstacle treated as static.** Broken mode predicts zero obstacle velocity. It chooses a straight path because the initial obstacle is off-axis, but actual motion puts both bodies at the crossing together.

## Explanation and recovery

Restore measured obstacle velocity in the relative-motion equation, select the least-deviating safe candidate, and replay the actual encounter. Real systems also need uncertainty, acceleration bounds, and receding-horizon updates.

## Common mistakes

- Checking geometric path intersection without checking time coincidence.
- Using absolute rather than relative velocity in closest-approach time.
- Looking beyond the model-valid prediction horizon.
- Calling a constant-velocity safe candidate collision-proof under arbitrary acceleration.

## Focused check and teach-back

At baseline, cite selected heading, closest separation, and CPA time. Freeze predicted obstacle motion, observe the safety violation, recover it, and teach back the relative frame, units, horizon limit, and candidate-selection rule.
