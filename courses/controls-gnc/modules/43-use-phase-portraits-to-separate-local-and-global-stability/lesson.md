# Use Phase Portraits to Separate Local and Global Stability

The double-well oscillator has equilibria at x=−1, 0 and +1 m. Use unit mass, linear stiffness coefficient 1 kg/s² and cubic coefficient 1 kg/(m² s²). Its two wells are locally stable for positive damping, while the origin is a saddle. Integrating the actual equations reveals which well a finite-energy trajectory approaches.

## Model and equations

\[
E=\frac{v^2}{2}-\frac{x^2}{2}+\frac{x^4}{4},\qquad \dot{E}=-cv^2
\]

`dx/dt=v; dv/dt=x-x^3-c*v`

`E=v^2/2-x^2/2+x^4/4; dE/dt=-c*v^2`

`well characteristic: lambda^2+c*lambda+2=0`

Worked example: At x=0 and initial energy 0.8 J, v=sqrt(1.6)=1.264911 m/s. With c=0.25/s, the initial energy rate is −0.4 W. The well poles have real part −0.125/s; the origin still has one unstable pole.

## Baseline workflow

Will positive damping force every initial condition toward the +1 m well? Use the phase portrait and the energy barrier at E=0 to justify your prediction.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Double-well phase portrait plots the integrated x-v trajectory and all three equilibria. Mechanical energy balance compares computed energy with initial energy plus integrated damping work. The mean power metric averages the actual six-second energy change.

## Two one-variable sweeps

Raise damping from 0.25 to 1/s and inspect crossings and energy decay. Reset, then raise initial energy from 0.8 to 2.5 J and inspect how long the trajectory can cross the central barrier.

## Intentionally broken case

Broken mode negates the selected damping, retaining the selected initial energy. Energy is supplied at +|c|v² rather than dissipated; the growing trajectory is integrated rather than replaced by an exponential sinusoid.

## Recovery

Restore positive damping and reset both controls. Check energy does not increase and the energy-work residual is small relative to the energy scale.

## Limiting cases and invariants

- For c=0, mechanical energy is conserved.
- At either well with v=0 the state remains at equilibrium.
- Energy decay alone does not establish global convergence to a particular well; the saddle and its invariant set remain.

## Independent evidence

Production uses explicit DOP853 on state plus damping work. Independent implicit Radau integrates the two physical states, then derives terminal energy and well distance. Tests also check the energy-work identity. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

A local eigenvalue describes a neighborhood, not every initial condition. Do not put energy in joules and power in watts on one undifferentiated axis.

## Teach-back

Explain why decreasing energy can coexist with switching wells early in the trajectory. What equation would a fabricated phase curve fail?

Answer rationale: While E is above the zero-energy barrier, crossings are possible even with dissipation. The actual phase curve must satisfy x_dot=v and v_dot=x−x³−cv, with E−E0 equal to accumulated −cv² work.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
