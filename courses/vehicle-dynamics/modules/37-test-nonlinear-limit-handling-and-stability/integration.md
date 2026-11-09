# From a moment slice to a stability claim

The original yaw-moment plot holds yaw rate at a kinematic value while sweeping sideslip. Its derivative is a useful component diagnostic. It is **not** a stability test of the coupled vehicle and does not establish recoverability. The two-state study below executes the additional dynamics needed to examine that claim.

## Derive the state equations

Use forward-left body axes and positive left yaw. Let beta be body sideslip in radians, r yaw rate in radians/s, and constant forward speed v = 28 m/s. For mass m = 1450 kg and yaw inertia Iz = 2400 kg m², the small-body-angle balances are

$$\dot\beta=\frac{F_{yf}+F_{yr}}{mv}-r,\qquad \dot r=\frac{aF_{yf}-bF_{yr}}{I_z}.$$

The axle distances are a = 1.2 m and b = 1.5 m. Front slip is delta − beta − ar/v; rear slip is −beta + br/v. The same bounded tanh tire relation now receives the **current dynamic yaw rate**, rather than the imposed kinematic yaw rate of the component plot. Static axle loads sum to mg. No load transfer, longitudinal speed change, tire relaxation, steering actuator, or combined-slip demand is included here.

At equilibrium both derivatives must vanish. A zero yaw moment alone is insufficient: lateral force must also equal mvr. The bounded least-squares solve checks both residuals, with yaw scaled by a declared one-second time scale. An equilibrium is accepted only if its scaled residual is below 1e-8 rad/s and its sideslip is strictly inside ±0.35 rad. A failed solve is reported as unavailable. Its zero margin placeholder has no stability interpretation.

## Local linearization and a falsifiable prediction

Differentiate the tire law: dFy/dalpha = C sech²(C alpha/(mu Fz)). Use the chain rule through both slip angles to construct the full 2×2 Jacobian. As an axle saturates, this effective slope falls even though the nominal C is unchanged. Local asymptotic stability requires both eigenvalues to have negative real parts; the reported decay margin is minus the largest real part. Positive margin establishes only local behavior about a valid trim.

For a force-balance estimate at r = 0.2 rad/s, the required total lateral force is 1450 × 28 × 0.2 = 8120 N. Zero yaw moment then requires front force 4511.11 N and rear force 3608.89 N. Compare these demands with each axle's mu Fz before trying to infer a realizable trim. Even a stable linear solution is inadmissible if it needs force beyond capacity.

## Execute, compare and recover

The new plots start from zero sideslip and yaw rate and integrate a constant-steer response for three seconds with fourth-order Runge–Kutta at 5 ms. The trajectory stops before a sampled state exceeds |beta| = 0.35 rad or |r| = 1.5 rad/s; the completion flag then becomes false. This is a declared model-domain cutoff, not a simulation of a spin beyond the cutoff. The utilization trace exposes whether the linear broken model demands impossible axle forces.

First hold friction fixed and raise steer; predict changes in trim, effective tire slopes and transient utilization. Then restore steer and reduce friction. Distinguish an unavailable trim from an unstable trim, a locally stable trim from a globally recoverable vehicle, and an incomplete domain-limited trajectory from a completed one. Record the last valid time for an incomplete trajectory. Restore healthy mode and check the same trim residual, time history and utilization at identical inputs.

The independent check solves lateral-velocity/yaw equations with an adaptive integrator, compares every retained state, verifies the analytic Jacobian by finite perturbations, and tests step refinement. These are numerical checks of this synthetic model. They do not validate tire parameters or certify a car, driver, controller or maneuver.
