# Evaluate grasp contacts and force closure

A gripper does not control an object merely because two fingertips touch it. Contact normals, friction, moment arms, and admissible force directions determine which external wrenches the grasp can oppose. This laboratory builds a planar grasp map from two frictional point contacts and asks two separate questions: does the contact set surround the origin in wrench space, and can nonnegative contact intensities balance a specified load? Keeping those questions separate prevents a common engineering error in which matrix rank is mistaken for physical force closure.

## Model, derivation, and conventions

All vectors are expressed in one object-fixed planar frame. A contact at position `r=[r_x,r_y]` has an inward unit normal `n` and tangent `t=[-n_y,n_x]`. The Coulomb cone is approximated by its two edge forces, `f=n+mu t` and `f=n-mu t`. Each edge contributes the scaled planar wrench `g=[f_x,f_y,(r_x f_y-r_y f_x)/r_o]`. Dividing moment by object radius `r_o` gives all three rows force units, so a Euclidean residual has the interpretable unit newtons.

Stacking the four edge wrenches gives a `3 by 4` grasp matrix `G`. Planar force closure requires full row rank and a vector `alpha` with every component strictly positive such that `G alpha=0`. The null-space vector is normalized to unit sum, and its smallest coefficient becomes the signed closure margin. The experiment also solves `min ||G lambda-w_ext||^2` subject to `lambda>=0` with projected gradient descent. The final residual tests a particular external load; the positive equilibrium tests load-independent local closure.

## Predict before running

Before moving a control, predict what lower friction does. The cone edges rotate toward each contact normal, so tangential force and torque authority shrink. The grasp matrix may remain rank three even while its positive-equilibrium margin becomes small. Then predict the named broken case: the second contact normal points outward. Its wrench columns still contain varied force and moment directions, so a numerical rank test may look healthy. Yet the columns cannot all participate positively in a self-equilibrating squeeze. The signed margin should become nonpositive and the nonnegative load residual should grow sharply.

## Baseline workflow

Run the baseline with friction coefficient `0.6` and eight degrees of contact misalignment. Inspect the four force-generator traces. They show directions in the object force plane; the missing moment coordinate remains present in the calculations and metrics. Confirm that the closure margin is positive. A positive value means all four cone edges contribute to a zero resultant rather than relying on tension or a negative contact intensity.

Next inspect the projected-gradient residual. It should descend monotonically toward a small value as contact intensities are projected onto the nonnegative orthant. The reported contact effort is the sum of edge coefficients for the selected equivalent external wrench. It is not a motor-current prediction: fingertip geometry, compliance, transmission efficiency, and actuator limits are outside this compact model.

## Two one-variable sweeps

For sweep one, reduce only the friction coefficient from `0.6` to `0.25`. Contact positions, load, solver iterations, and normal conventions remain unchanged. The narrower cones should reduce the positive equilibrium margin and generally require greater effort or leave a larger load residual. This is a controlled comparison of frictional authority, not a comparison of different grasps.

For sweep two, restore friction to `0.6` and increase only the angular contact misalignment to twenty-five degrees. One contact is no longer perfectly antipodal to the other. The moment arms and inward normals therefore lose symmetry. Observe the closure margin and load solution together. A grasp can remain force closing while becoming less robust to coefficient error. That distinction matters when perception supplies uncertain contact locations.

## Intentionally broken case

Broken mode reverses the second inward normal but leaves the rest of the arithmetic intact. This models a frame or surface-normal sign error, not a low-friction surface. The generated columns can still span three algebraic directions, which is why rank alone is insufficient. Physical contacts can push but cannot pull. A negative coefficient in the equilibrium combination would ask a fingertip to attract the object through a unilateral point contact.

The failure is deliberately subtle: array shapes are correct, singular-value decomposition succeeds, and the load solver returns finite coefficients. Only the positivity condition and residual expose that the model no longer represents a realizable squeeze. Production grasp pipelines should validate normal orientation against the object surface and visualize it during review.

## Recovery

Recover by expressing positions, normals, tangents, and external loads in the same object frame. Orient every normal into the object, generate both friction-cone boundaries, and retain the unilateral `lambda>=0` constraint. Require rank three, a small equilibrium residual, and strictly positive normalized coefficients before calling the planar grasp force closing. Then test task-specific loads with force limits rather than assuming closure guarantees unlimited capacity.

If measured contact uncertainty can flip a margin sign, treat the grasp as fragile. Widening a numerical tolerance is not recovery. Better responses include choosing new contact sites, increasing commanded normal force within safe limits, adding a contact, or reducing the anticipated external wrench.

## Alternative and limiting cases

An exact planar friction cone can be handled as a second-order cone instead of two edges. In three dimensions, polyhedral pyramids or conic optimization operate on six-dimensional wrenches. Grasp quality measures may use the radius of the largest origin-centred ball in the convex hull, minimum singular values, or task-wrench-space coverage. The positive-null test used here is intentionally inspectable and appropriate for four planar generators.

With zero friction, each cone collapses to a normal ray and the pair cannot resist arbitrary planar torque. With perfectly antipodal contacts, the equilibrium is symmetric. With coincident contacts, moment authority collapses regardless of rank errors caused by scaling. With infinite friction, the point-contact model itself becomes questionable because torsional contact, finite patches, and material limits dominate.

## Independent evidence and MATLAB-style design boundary

The independent reference reconstructs both contact frames, forms its own wrench matrix, obtains the null-space equilibrium, and separately executes the projected nonnegative load solve. It imports no production experiment, consumes no production result, and perturbs no production value. Expected and production signatures are retained for the baseline, friction sweep, misalignment sweep, reversed-normal failure, and exact recovery.

This is deterministic NumPy software evidence. No MATLAB optimization routine, force-torque sensor, tactile array, contact identification, compliance model, browser accessibility study, learner trial, physical HIL, safety certification, or deployment was run. The laboratory teaches the mechanics boundary; it does not certify a real gripper.

## Engineering review checklist

- Express every contact position and force direction in one declared frame.
- Verify that surface normals point into the object and tangents use a consistent handedness.
- Scale force and moment rows before comparing residual magnitudes.
- Check positive equilibrium in addition to matrix rank.
- Preserve unilateral nonnegative contact intensities in load solves.
- Compare requested contact effort with actuator and material limits.
- Propagate contact-location, normal, and friction uncertainty into the margin.
- Report failure when a task wrench lies outside the feasible cone.

## Common mistakes

Common mistakes include using outward normals, swapping the cross-product order, mixing metres and millimetres in the moment row, normalizing wrench columns inconsistently, or interpreting a singular value as a unilateral feasibility proof. Another error is to solve an unconstrained least-squares problem and accept negative contact forces. A tiny residual from that solve can be physically meaningless. Engineers also overstate a positive local force-closure test as proof against slip, crushing, rolling contact, actuator saturation, or uncertain dynamics.

## Focused check and teach-back

Explain why four columns can span three-dimensional planar wrench space and still fail to surround the origin with positive weights. Identify the unit carried by the scaled moment row. Then teach back the difference between closure margin and task-load residual: one asks whether small wrenches in every direction are locally resistible, while the other asks whether this finite generator set can balance one selected wrench with nonnegative intensity. Finally, name the exact recovery for the broken case and explain why merely increasing friction cannot repair an outward normal convention.
