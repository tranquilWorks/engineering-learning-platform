## P43 evidence task

Explain why decreasing energy can coexist with switching wells early in the trajectory. What equation would a fabricated phase curve fail?

Before running: Will positive damping force every initial condition toward the +1 m well? Use the phase portrait and the energy barrier at E=0 to justify your prediction.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Double-well phase portrait plots the integrated x-v trajectory and all three equilibria. Mechanical energy balance compares computed energy with initial energy plus integrated damping work. The mean power metric averages the actual six-second energy change.

### Reasoning rubric

- Model: use `dx/dt=v; dv/dt=x-x^3-c*v` to explain the observed quantity rather than repeating a metric label.
- Evidence: For c=0, mechanical energy is conserved. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode negates the selected damping, retaining the selected initial energy. Energy is supplied at +|c|v² rather than dissipated; the growing trajectory is integrated rather than replaced by an exponential sinusoid. Identify the measured consequence in your record.
- Recovery and scope: Restore positive damping and reset both controls. Check energy does not increase and the energy-work residual is small relative to the energy scale. State this limit: Energy decay alone does not establish global convergence to a particular well; the saddle and its invariant set remain.

### Check your explanation

While E is above the zero-energy barrier, crossings are possible even with dissipation. The actual phase curve must satisfy x_dot=v and v_dot=x−x³−cv, with E−E0 equal to accumulated −cv² work.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
