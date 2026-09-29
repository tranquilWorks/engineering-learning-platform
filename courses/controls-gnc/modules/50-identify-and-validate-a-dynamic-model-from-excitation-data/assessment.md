## P50 evidence task

Why can the broken training fit look plausible while held-out prediction fails? How do you distinguish free-run validation from one-step fitting?

Before running: Could a tiny training residual coexist with a useless input coefficient? Predict what removing training excitation does to regressor rank.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Separate held-out validation compares truth with a free-running fitted model. Training data and fitted response displays the excitation, measured next output and one-step fit. Rank and smallest singular value reveal information loss; parameter error uses known synthetic truth.

### Reasoning rubric

- Model: use `y[k+1]=0.82*y[k]+0.18*u[k]+0.002*cos(1.7*k)` to explain the observed quantity rather than repeating a metric label.
- Evidence: With nondegenerate excitation and zero disturbance, least squares recovers the exact coefficients. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode removes the training input while leaving the held-out excitation active. The second regressor column is zero, b is unidentifiable, and the least-squares minimum-norm result sets it to zero. Identify the measured consequence in your record.
- Recovery and scope: Restore excitation and reset controls. Confirm rank two, a positive smallest singular value and a fitted model that predicts held-out dynamics using its own previous predictions. State this limit: Held-out RMSE is a finite synthetic experiment result, not a guarantee for untested plants or noise processes.

### Check your explanation

With u=0, training contains no evidence about b. Held-out input exposes that missing coefficient. Free-run prediction feeds back y_hat; one-step fitting uses measured y and can conceal drift.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
