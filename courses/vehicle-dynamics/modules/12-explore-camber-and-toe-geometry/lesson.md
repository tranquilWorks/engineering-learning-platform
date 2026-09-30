# Estimate Camber Thrust and Toe Scrub

Which force and power estimates can this simple alignment model support?

## Physical model

This lesson is deliberately limited to empirical camber thrust and toe scrub. It does not calculate suspension kinematics. Convert input camber γ and toe τ from degrees to radians. With a camber coefficient C_γ = 60000 N/rad, load scale F_z = 3600 N and speed V = 20 m/s:

F_camber = −C_γ γ; F_scrub = F_z |tan τ|; P_scrub = V F_scrub.

Camber thrust is signed; negative camber gives positive force under the declared convention. Scrub force and power are nonnegative loss magnitudes and are even in toe. Force and power use separate metrics and curves. The response shows signed camber force in N against camber degrees at the selected conversion mode. Toe is an independent input here, so changing toe does not change that response curve.

The power equation has units (m/s)N = W. It estimates dissipative demand but contains no tire thermal mass, heat transfer or temperature state. A large power value cannot be translated into a temperature without another model.

\[
F_{\mathrm{camber}}=-C_\gamma\gamma,\qquad F_{\mathrm{scrub}}=F_z|\tan\tau|,\qquad P=VF_{\mathrm{scrub}}.
\]

## Worked baseline

At camber −2° and toe +0.1°, γ = −0.0349066 rad and τ = 0.00174533 rad. Camber thrust is about +2094.40 N, scrub force 6.28319 N and scrub power 125.664 W. Reversing toe leaves scrub and power unchanged; reversing camber reverses thrust. Zeroing only toe removes scrub power but does not remove camber thrust.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold toe at +0.1° and vary camber from −5° to +2°. Predict a straight decreasing force curve with slope −60000π/180 ≈ −1047.20 N/deg. Locate its zero crossing and explain why toe power remains unchanged.
2. Restore camber to −2° and sweep toe from −0.5° through zero to +0.5°. Predict an even, nonnegative scrub-power curve with a minimum at zero. It is approximately proportional to |toe| at these small angles, not signed toe. Read its vertical axis in W rather than N.

## Named broken behavior

The toggle treats the degree numbers directly as radians. The default −2° value becomes −2 rad in the constitutive law, producing a false 120000 N camber thrust. The 0.1 toe input becomes 0.1 rad, producing about 361.205 N scrub and 7224.10 W. This executes the conversion fault in both force laws; it does not simply flip a validity flag. With both angles zero, nominal and faulty results coincide. Nonzero angles are needed to test conversion.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The camber law is linear, empirical and uncapped. At sufficiently large camber it can predict force beyond a plausible friction limit; no friction-circle enforcement is present in this lesson. Toe scrub is a geometric loss estimate, not a combined-slip tire solution. The model omits suspension travel, compliance steer, contact-patch changes, temperature and tire wear. Even a dimensionally correct output is not measured-vehicle validation.

## Common mistakes

Do not infer a full camber curve through suspension travel from two static alignment inputs. Do not report watts as heat in joules or as temperature. Squaring a small angle would change this model's intended near-zero |toe| dependence.

## Formative checks

Compare camber ±2° with toe ±0.1°, then set one angle at a time to zero. Record force and power units and parity. Activate the degree/radian fault at the defaults and explain why its camber-force ratio differs from its scrub-power ratio.

Check your reasoning: Camber force is odd in camber; toe scrub and power are even in toe. The camber error factor is exactly 180/π because that law is linear, whereas tan makes the scrub ratio nonlinear. A complete response separates the two mechanisms and declines to infer temperature or full suspension geometry from these estimates.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
