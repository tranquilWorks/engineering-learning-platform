# Balance Longitudinal Load Transfer

Can axle loads add to vehicle weight and still be physically inconsistent?

## Physical model

Let m = 1320 kg, L = 2.57 m and the static front weight fraction be 0.53. Front and rear axle loads at rest are 0.53mg and 0.47mg. Positive longitudinal acceleration shifts normal force rearward through the pitch moment m a_x h:

ΔF = m a_x h/L; F_zf = 0.53mg − ΔF; F_zr = 0.47mg + ΔF.

Two independent balances matter. Vertical balance requires F_zf + F_zr = mg. Pitch balance requires L(0.53mg − F_zf) = m a_x h. Satisfying the first does not imply satisfying the second. The response plots both axle loads in N against acceleration in m/s² at the selected centre-of-gravity height. The displayed transfer is the demanded shift between axles, not extra vehicle weight.

The front and rear lines have opposite slopes and their sum is constant. Their asymmetry about equal load comes from the chosen static distribution, not from a loss of vertical balance.

\[
\Delta F=\frac{ma_xh}{L},\qquad F_{zf}=0.53mg-\Delta F,\quad F_{zr}=0.47mg+\Delta F.
\]

## Worked baseline

At 4 m/s² and h = 0.5 m, total weight is 12949.2 N and transfer is 1027.23735 N. The front axle carries 5835.83865 N and the rear 7113.36135 N. Multiplying the transfer by 2.57 m gives 2640 N·m, equal to 1320 × 4 × 0.5. Under −4 m/s² braking, transfer changes sign: the front gains what the rear loses. The static values themselves do not exchange.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Keep h = 0.5 m and sweep acceleration from −9 to +9 m/s². Predict a straight decreasing front-load line and increasing rear-load line. Locate zero acceleration, then check the vertical sum at two unequal acceleration values.
2. Hold acceleration at +4 m/s² and vary height from 0.25 to 0.85 m. Predict more rearward transfer as height rises. Repeat mentally for braking: the front-load trend with height would reverse. The secondary sweep follows the selected acceleration, so its slope can change sign.

## Named broken behavior

The fault ignores acceleration-induced transfer and returns the two static axle loads. Their sum still equals weight, which makes a total-load-only test misleading. At the defaults, the pitch residual has magnitude 2640 N·m. Both fault response lines become horizontal with acceleration. At zero acceleration, omission is genuinely benign: demanded transfer is zero. Use a nonzero excitation to diagnose the fault.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The calculation is a quasi-static two-contact balance. It neglects pitch acceleration, suspension motion, road slope, aerodynamic moments and unsprung-mass details. A predicted negative axle load means contact assumptions have failed; it is not a realizable downward tire reaction. All declared nominal control corners retain positive loads, so wheel lift is a boundary to derive, not an event observed in this range. Front lift would require a_x = 0.53gL/h.

## Common mistakes

A car does not gain total weight during acceleration. Redistribution changes axle loading while the total remains mg. Checking only the sum can allow an incorrect distribution to pass; moment closure is essential.

## Formative checks

Compare +4 and −4 m/s² at h = 0.5 m. Calculate both axle loads and verify vertical and pitch balance. Activate the fault at +4 m/s². Explain why one balance passes and the other fails, then identify an input at which that fault becomes invisible.

Check your reasoning: The transfer magnitude is 1027.23735 N, reversing with acceleration. Both nominal balances close. Omission preserves total weight but misses the nonzero pitch moment; zero acceleration hides it. Credit requires a signed transfer and a moment in N·m, rather than only a statement that the rear load should increase.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
