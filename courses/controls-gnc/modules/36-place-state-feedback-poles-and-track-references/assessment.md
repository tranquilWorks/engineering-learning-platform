## P36 evidence task

At x=0.5 m, v=0.4 m/s, which trace supplies 1.6 m/s², and why does the other show 4? Explain why the fault changes the endpoint without moving a pole.

Before running: Will changing only Nbar move the poles? Predict the final position with Nbar=1/s² before enabling the fault.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Reference tracking shows position and the one-metre command. Full feedback command compares the acceleration that actually drives the states with the incomplete position-only expression. They differ whenever velocity is nonzero.

### Reasoning rubric

- Model: use `dx/dt=v; dv/dt=u` to explain the observed quantity rather than repeating a metric label.
- Evidence: At zero velocity, the complete and incomplete command expressions coincide. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode uses Nbar=1/s² while retaining K and both propagated states. The baseline final-value position becomes 1/8 m even though both poles remain stable. Identify the measured consequence in your record.
- Recovery and scope: Disable broken mode and reset both controls. Check steady tracking error returns to zero and compare the two acceleration traces again. State this limit: A finite plotted endpoint need not equal the exact final value; the DC metric uses the equilibrium.

### Check your explanation

The complete command includes −6v=−2.4 m/s². Nbar changes the forced equilibrium Nbar/k_p; K fixes the characteristic polynomial. A correct explanation separates dynamics from command scale.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
