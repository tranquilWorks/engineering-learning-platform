# Reconstruct a Driven Trajectory

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. The speed, yaw, and position-correction streams are deterministic and synthetic.

## Model and equations

- `psi[k+1]=psi[k]+r[k]Delta_t`
- `p_predict[k+1]=p[k]+v[k][cos(psi[k]),sin(psi[k])]Delta_t`
- `p[k+1]=p_predict[k+1]+K_gps(p_gps[k+1]-p_predict[k+1])Delta_t`

Heading and yaw rate are stored in radians during integration. East-north position uses forward speed rotated by the prior-step heading.

## Baseline workflow

Integrate the declared yaw-rate stream, project forward speed into inertial axes, apply bounded position correction, and compare the resulting path against an independently generated reference. Audit endpoint and full-trajectory closure.

## Two one-variable sweeps

Change only initial heading, then increase only position-correction gain. The first rotates the whole path; the second changes correction bandwidth without changing the kinematic path-length ledger.

## Intentionally broken case

Use degree-valued heading in trigonometric functions and integrate degrees per second as radians per second. The final heading label can look plausible while the path diverges.

## Recovery

Convert angular inputs to radians once, integrate with explicit timestamp spacing, retain a single body-to-inertial convention, and apply correction in position units.

## Limiting cases and invariants

- Zero correction gain gives pure dead reckoning.
- Zero yaw rate gives a straight path along initial heading.
- Integrated scalar path length is independent of heading representation.

## Independent evidence

A separate discrete integrator reconstructs truth, measurements, and corrected state for every scenario.

## Common mistakes

- Mixing degrees and radians inside the state.
- Using the updated heading with a prior-step speed without declaring the integration rule.
- Treating corrected position as an independent measurement truth.

## Formative checks

1. Why can path length remain correct when position is wrong?
2. What does closure RMS reveal beyond endpoint error?

## Teach-back

Explain the integration grid, angular units, coordinate convention, correction gain, broken path, and exact recovery.
