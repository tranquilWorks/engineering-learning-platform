# P69 course checkpoint

## Predict and derive

Connect visual pose, arm motion, grasp force and object placement.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_base=t_camera+R_camera*p_camera; cos(q2)=(norm(p)^2-l1^2-l2^2)/(2*l1*l2)`
- `F=k*x; positive spring work=max(0,k*(x_next^2-x_old^2)/2) J`
- `x_next<=sqrt(x_old^2+2*tank/k); commands require increasing source stamps and age<=0.04 s`
- `two-contact support margin=2*mu*10 N-4.4 N`

## Controlled comparison

- `vision_noise_cm`: 1.0 → 4.0. Hold the other controls at baseline and explain the mechanism before executing.
- `contact_friction_coefficient`: 0.6 → 0.3. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A grasp verdict must depend on executed arm/contact behavior and the object's final state; unrelated successful components do not prove integration.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Synthetic planar manipulation is not hardware or general 3D manipulation qualification.

Competency links: PHYSICAL-INTERACTION, MANIPULATION, SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
