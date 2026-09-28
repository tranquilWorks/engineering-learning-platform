# Perceive, reach, grasp, and regulate contact

This planar manipulation exercise joins camera calibration, two-link inverse kinematics, an idealized friction-support check and delayed force commands. The contact interface now experiences a real virtual dropout and an out-of-order packet; success depends on the resulting force, timestamps and energy.

## Model, derivation, and conventions

A camera observes $(0.72,0.18)$ m. Its base-frame translation is $(0.28,0.12)$ m and rotation is 25°. A deterministic vision perturbation equals the noise control in metres times $(0.5,-0.25)$. Transform the estimate with $\mathbf p_b=\mathbf t+R\mathbf p_c$ before solving links $l_1=0.75$ m and $l_2=0.55$ m:

\[\cos q_2=\frac{\|\mathbf p_b\|^2-l_1^2-l_2^2}{2l_1l_2},\qquad \mathbf p_{tip}=\begin{bmatrix}l_1\cos q_1+l_2\cos(q_1+q_2)\\l_1\sin q_1+l_2\sin(q_1+q_2)\end{bmatrix}.\]

The negative-elbow branch is used, then forward kinematics checks actual pickup error. Two ideal opposed contacts, each with 10 N normal force, support a 4.4 N vertical load if $2\mu(10)-4.4\ge0$ N. This is a static friction-support abstraction, not full wrench closure or a grasp simulation.

The contact spring has $k=600\,\mathrm{N/m}$ and desired force 10 N. At 100 Hz the healthy velocity demand is $\operatorname{clip}(0.012(10-F),-0.025,0.025)$ m/s. Commands arrive three ticks late; source ticks 80–95 are dropped, and source 50 reappears at tick 120. Increasing timestamps and a 0.04 s age limit gate application.

The tank starts at 0.18 J. Positive elastic work is

\[W_+=\max\{0,\tfrac12 k(x_{new}^2-x_{old}^2)\},\qquad x_{new}\le\sqrt{x_{old}^2+2E/k}.\]

This accounts for the first penetration even when initial force is zero. Released spring energy is not credited back to this conservative tank.

## Baseline workflow

Predict the spring energy needed for 10 N: penetration is $10/600=0.01667$ m, so stored energy is $10^2/(2\cdot600)=0.08333$ J. The initial tank can support it. Run the baseline and inspect the transformed approach, force through the timed gap and visible requirement table. Final tank energy is about 0.09667 J; pickup error is about 0.00559 m.

The table checks pickup ≤0.055 m, reachable geometry, nonnegative support margin, final force error ≤3 N, nonnegative tank energy, zero expired nonzero/source-inverted commands, and fresh post-gap force recovery. They are model-specific exercise requirements.

## Two one-variable sweeps

1. Keep friction fixed and increase vision noise from 1 to 4 cm. Predict pickup error from the norm of the deterministic perturbation: it grows fourfold, while the independently modeled force loop stays unchanged.
2. Restore vision noise and reduce friction from 0.6 to 0.3. Read the support margin in newtons. Both settings may pass and leave the three summary metrics unchanged; the actual grasp requirement quantity still changes.

## Intentionally broken case

Broken mode omits the camera extrinsic, uses positive contact feedback, bypasses the energy guard and accepts stale commands. Penetration reaches its 0.05 m bound, giving 30 N and 0.75 J spring energy. Starting from 0.18 J therefore yields a minimum tank near −0.57 J: this is a measured energy violation, not a preset failure flag.

## Recovery

Restore healthy mode at the same vision and friction settings. The source-time guard, correct transform, negative force feedback and exact work bound return. Force and tank histories must reproduce the baseline.

## Alternative and limiting cases

With zero initial tank energy in the internal limiting test, no positive penetration is possible, including the first contact step. Zero vision perturbation gives geometric closure to numerical tolerance. Friction below 0.22 cannot support the stated load even if reach and force regulation pass. During expiry, healthy applied velocity is zero.

## Independent evidence and MATLAB-style design boundary

The reference uses complex-plane pose/kinematic formulas, reconstructs source arrivals and debits trapezoidal spring-force work. That work equals the exact elastic-energy change but follows a different calculation. Five independent scenarios and zero-energy/timestamp tests cover the original false recovery claim.

## Common mistakes

Do not calculate initial work using only the old zero force, infer frictional support from successful IK, or report interface recovery merely because broken mode is off.

## Focused check and teach-back

- Why does old-force times displacement miss energy? Force increases during penetration; its average is not the initial value.
- Why can noise alter pickup while force stays unchanged? The declared contact model regulates a separate local axis after approach.
- What proves interface recovery? Fresh accepted post-gap commands and measured final force, with no expired nonzero application.

## Cumulative assessment

Derive the frame transform and required spring energy, trace the dropped-command interval into the watchdog, and identify each failed broken-run requirement from its computed quantity. Explain the static-support and planar-contact limits before generalizing to a real robot.

## Predict before running

Write down the frame in which each position is expressed before solving any joint angle. Predict whether omitting the 25° camera rotation changes only the plotted estimate or also the actual commanded endpoint. Then compute the energy needed for first contact and for the 10 N target. Finally, mark the source-command dropout on a time axis and distinguish its first missing source tick from the last still-valid delivered command.

## Engineering review checklist

Derive the energy guard from work, not from a software flag. For a linear spring, $F(x)=kx$ and $\int_{x_a}^{x_b}F(x)dx=k(x_b^2-x_a^2)/2$. Requiring this increase to be at most the available tank gives the square-root penetration bound. At $x_a=0$, the old force is zero but the integral is positive for every positive $x_b$. This is why an old-force-only rectangle rule falsely permits free energy at first contact. Trapezoidal force integration is exact for this linear spring and supplies the independent formulation.

Trace the timing fault using integer ticks. Source 79 arrives at receiver tick 82. Sources 80 through 95 are missing; at tick 84 the most recent source is five ticks old, so healthy command application becomes zero. Source 96 arrives at tick 99 and can resume feedback. Later, at tick 120, the duplicate source 50 must not replace the newer accepted command. The retained source and age columns let you check these events without trusting a prewritten recovery verdict.

Distinguish the delivered velocity command from the realized penetration. The watchdog gates the command; the tank and penetration bounds may further restrict motion. A controller asking for positive velocity does not prove the spring gained the requested displacement. Check force and elastic work from the actual new penetration.

Finally, separate the kinematic approach, ideal static support and one-axis contact assumptions. The straight approach trace is not a collision-aware motion plan; two fixed normal contacts are not a full spatial grasp wrench set; and the virtual spring is not measured compliance. Successful integration here means the declared calculations and timed interface agree, with these boundaries retained.
