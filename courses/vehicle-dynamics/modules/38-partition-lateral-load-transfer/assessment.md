# P38 course checkpoint

## Predict and derive

Derive wheel loads from the transferred amount and detect when a four-contact equilibrium becomes impossible.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `M_roll=m a_y h`
- `Delta F_z,f t_f+Delta F_z,r t_r=M_roll`
- `M_elastic=M_roll-M_geometric`
- `Fz_inner=W/2-T; Fz_outer=W/2+T; T*track=M; four-contact domain |T|<=W/2`

## Controlled comparison

- `lateral_accel_g`: 1 → 1.4. Hold the other controls at baseline; predict and explain the change before executing.
- `front_roll_stiffness_fraction`: 0.58 → 0.7. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

If T is the load moved, inner load is W/2-T and outer load W/2+T; their difference is 2T. Multiplying that difference by half-track gives T*track, the roll moment. Using +/-T/2 halves the moment and underestimates the load-sensitive capacity loss. First subtract geometric moment from total before distributing the elastic remainder. A negative requested inner load marks lift-off: the displayed capped capacity is only a bound and cannot close the original four-contact equilibrium.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The model has no post-lift-off roll dynamics or changed contact geometry. A zero moment residual in the demanded ledger cannot override a nonzero contact-excess flag.

Competency links: VD-FORCE-BALANCE, VD-HANDLING-NONLINEAR, VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
