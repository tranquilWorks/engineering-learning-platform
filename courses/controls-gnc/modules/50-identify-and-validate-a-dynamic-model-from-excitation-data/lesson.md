# Identify and Validate a Dynamic Model from Excitation Data

Identification quality depends on actual excitation, regressor information and validation outside the fitting data. This deterministic synthetic ARX experiment has a 0.02-second sample period, known coefficients and a small unmodeled periodic disturbance. It provides measured model errors, not statistical confidence bounds.

## Model and equations

\[
\hat\theta=\operatorname*{arg\,min}_{\theta}\|X\theta-y_{next}\|_2^2
\]

`y[k+1]=0.82*y[k]+0.18*u[k]+0.002*cos(1.7*k)`

`[a_hat,b_hat]=argmin ||X*theta-y_next||_2; X=[y_current,u]`

`held-out y_hat[k+1]=a_hat*y_hat[k]+b_hat*u[k]`

Worked example: The plant has a=0.82 and b=0.18. A 300-sample multisine experiment builds X from current output and input. A distinct 200-sample experiment uses changed frequencies/phases and resets its initial state; indices 300–499 are never used for fitting.

## Baseline workflow

Could a tiny training residual coexist with a useless input coefficient? Predict what removing training excitation does to regressor rank.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Separate held-out validation compares truth with a free-running fitted model. Training data and fitted response displays the excitation, measured next output and one-step fit. Rank and smallest singular value reveal information loss; parameter error uses known synthetic truth.

## Two one-variable sweeps

Raise excitation amplitude from 1 to 3 and inspect singular value and validation error. Reset, then raise frequency spread from 2 to 5 Hz and inspect the new waveform and fit; conditioning and error need not change monotonically together.

## Intentionally broken case

Broken mode removes the training input while leaving the held-out excitation active. The second regressor column is zero, b is unidentifiable, and the least-squares minimum-norm result sets it to zero.

## Recovery

Restore excitation and reset controls. Confirm rank two, a positive smallest singular value and a fitted model that predicts held-out dynamics using its own previous predictions.

## Limiting cases and invariants

- With nondegenerate excitation and zero disturbance, least squares recovers the exact coefficients.
- With zero training input, no amount of output fitting identifies the input gain.
- Held-out RMSE is a finite synthetic experiment result, not a guarantee for untested plants or noise processes.

## Independent evidence

Independent convolution constructs observations; a two-by-two normal-equation calculation fits coefficients and convolution predicts held-out response. Production uses scalar propagation and SVD least squares. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Teacher-forcing held-out measurements into every prediction hides accumulated model error. An error measured against synthetic truth is not a confidence interval.

## Teach-back

Why can the broken training fit look plausible while held-out prediction fails? How do you distinguish free-run validation from one-step fitting?

Answer rationale: With u=0, training contains no evidence about b. Held-out input exposes that missing coefficient. Free-run prediction feeds back y_hat; one-step fitting uses measured y and can conceal drift.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
