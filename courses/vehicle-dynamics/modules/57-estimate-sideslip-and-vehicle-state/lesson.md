# Estimate Sideslip and Vehicle State

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses a bounded synthetic two-state vehicle model and deterministic measurement disturbance.

## Model and equations

- `x_predict[k+1]=x_hat[k]+Delta_t(A x_hat[k]+B delta[k])`
- `innovation[k+1]=z[k+1]-x_predict[k+1]`
- `x_hat[k+1]=x_predict[k+1]+K innovation[k+1]`

The state is ordered as sideslip angle, yaw rate, then steering-bias state, all in radians internally. A diagonal innovation gain closes measured state error while a deterministic covariance ledger tracks remaining uncertainty.

## Baseline workflow

Propagate the truth state, add known disturbance, predict from steering, form innovations, correct the estimate, and compare sideslip and yaw RMSE. Inspect innovation RMS and final covariance trace together.

## Two one-variable sweeps

Increase only observer gain, then increase only measurement disturbance. Gain changes responsiveness and noise following; disturbance changes innovation and estimation error at fixed dynamics.

## Intentionally broken case

Reverse the measured sideslip sign. The observer remains numerically bounded yet converges toward a physically incompatible state.

## Recovery

Declare state order, sign, and units at each interface; predict on the timestamp grid; subtract prediction from measurement; and update state and uncertainty consistently.

## Limiting cases and invariants

- Low gain emphasizes model prediction.
- High gain follows measurement disturbance more closely.
- Stable eigenvalues do not repair a sign-convention error.

## Independent evidence

A separately written state propagation and correction loop recomputes all six retained diagnostics for five scenarios.

## Common mistakes

- Swapping sideslip and yaw-rate state order.
- Reversing lateral sign at only one interface.
- Reporting a covariance that is not updated with the estimator.

## Formative checks

1. Why is bounded output insufficient evidence of correct estimation?
2. How does gain change innovation use?

## Teach-back

Explain prediction, innovation, correction, covariance, state conventions, the reversed-sign failure, and recovery.
