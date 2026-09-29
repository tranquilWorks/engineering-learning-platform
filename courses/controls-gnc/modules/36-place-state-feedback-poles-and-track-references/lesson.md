# Place State-Feedback Poles and Track References

Pole placement specifies how initial errors decay. Reference tracking is a separate forced-response calculation. Here the plant is a double integrator with position in metres, velocity in m/s and commanded acceleration in m/s².

## Model and equations

\[
\dot{x}=v,\qquad \dot{v}=-k_p x-k_d v+\bar{N}r
\]

`dx/dt=v; dv/dt=u`

`u=-k_p*x-k_d*v+Nbar*r; k_p=p1*p2; k_d=p1+p2`

`Nbar=k_p gives x(infinity)=r`

Worked example: At p1=2/s and p2=4/s, k_p=8/s² and k_d=6/s. A one-metre reference requires Nbar=8/s². At x=0.5 m and v=0.4 m/s, u=8−8(0.5)−6(0.4)=1.6 m/s². Omitting velocity would incorrectly report 4 m/s².

## Baseline workflow

Will changing only Nbar move the poles? Predict the final position with Nbar=1/s² before enabling the fault.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Reference tracking shows position and the one-metre command. Full feedback command compares the acceleration that actually drives the states with the incomplete position-only expression. They differ whenever velocity is nonzero.

## Two one-variable sweeps

Increase dominant pole from 2 to 6/s at ratio 2: both position and velocity gains increase, in different units. Reset, then increase pole ratio from 2 to 5: the fast mode and command demand change while the healthy DC gain remains one.

## Intentionally broken case

Broken mode uses Nbar=1/s² while retaining K and both propagated states. The baseline final-value position becomes 1/8 m even though both poles remain stable.

## Recovery

Disable broken mode and reset both controls. Check steady tracking error returns to zero and compare the two acceleration traces again.

## Limiting cases and invariants

- At zero velocity, the complete and incomplete command expressions coincide.
- The feedback poles remain −p1 and −p2 regardless of Nbar.
- A finite plotted endpoint need not equal the exact final value; the DC metric uses the equilibrium.

## Independent evidence

An independent polynomial coefficient/DC calculation checks the signature; analytic two-exponential state derivatives check the whole acceleration history. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Do not add position and velocity gains into a norm labeled 1/s²: their dimensions differ. A stable homogeneous system can still track the wrong reference scale.

## Teach-back

At x=0.5 m, v=0.4 m/s, which trace supplies 1.6 m/s², and why does the other show 4? Explain why the fault changes the endpoint without moving a pole.

Answer rationale: The complete command includes −6v=−2.4 m/s². Nbar changes the forced equilibrium Nbar/k_p; K fixes the characteristic polynomial. A correct explanation separates dynamics from command scale.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
