# Portfolio Control Intake: Engineering Learning Platform

Create and govern `tranquilWorks/engineering-learning-platform` as a `product-data` repository.

## Intent

Build a reusable self-hosted engineering-learning platform that runs on one corporate network port and renders independent course folders as professional interactive lessons. The learner experience should closely match rich in-chat interactive learning blocks: concise content, prediction prompts, buttons/sliders/toggles/selectors, immediate numerical recomputation, linked advanced plots, dataframe-like tables, current-state explanations, and focused reflection.

## Product boundaries

- The platform is generic and must not hard-code DSP/radar behavior.
- Source course repositories remain canonical and are mounted/discovered read-only.
- Existing MATLAB modules are reference implementations and migration inputs, not the required learner-facing runtime.
- Native initial execution uses trusted Python with NumPy/SciPy/pandas.
- Plotly-compatible figure JSON is the initial advanced plotting contract.
- Arbitrary learner code, notebook uploads, and runtime package installation are prohibited until isolated workers are designed and reviewed.
- Production deployment is one unprivileged container/port behind existing corporate reverse proxy/SSO.

## Initial batches

1. Foundation vertical slice with React/Vite, FastAPI, course manifests, trusted runtime, Plotly/tables, P30 echo ranging, plotting gallery, tests, and Docker.
2. Contract hardening and schema migration.
3. MATLAB-first course inspection/scaffolding and golden vectors.
4. Author preview, visual regression, and accessibility.
5. Arrow/Parquet large-data transport.
6. Isolated experiment workers.
7. SSO-aware progress and assessments.
8. Runtime adapters, including optional licensed MATLAB Engine.
9. Corporate release readiness.
10. Representative course migrations before bulk conversion.

## Required claim boundary

Software simulation, schema, and deployment-configuration evidence only. Do not claim MATLAB equivalence, production corporate deployment, accreditation, hardware, real-time behavior, or operational validation without separately retained evidence.
