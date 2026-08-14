# Repository instructions

## Product purpose

This repository is the reusable presentation and execution platform for interactive engineering courses. It is not the canonical home for every course's subject-matter content, and it must not hard-code DSP/radar assumptions into generic platform components.

The learner experience must preserve the loop:

`short concept -> prediction -> manipulation -> immediate evidence -> explanation -> focused check -> next concept`

## Architectural boundaries

- `apps/web/` owns the professional learner-facing React UI and generic lesson components.
- `apps/api/` owns course discovery, schema validation, trusted experiment execution, result serialization, and production static serving.
- `packages/lesson-schema/` owns stable portable course/module contracts.
- `courses/` contains examples, templates, and optionally vendored courses. Independent course repositories may be mounted through `ELP_COURSE_PATHS`.
- Subject-specific calculations belong in course experiment functions, not generic UI components.
- MATLAB files are references or golden-vector sources unless an explicitly approved licensed MATLAB runtime adapter is added.

## Safety and trust boundaries

- Never execute arbitrary code supplied by a learner or uploaded through the browser.
- Python entrypoints are trusted repository or mounted-course code and must be validated at build/deploy time.
- Do not add `eval`, shell interpolation, unrestricted subprocess execution, dynamic package installation, or writable production course mounts.
- Keep production course mounts read-only.
- Large-compute and untrusted-authoring modes require an isolated worker design before implementation.
- Never claim MATLAB equivalence without retained comparison vectors or actual MATLAB execution evidence.

## Build-mode rules

- Read `contracts/active-batch.yaml` before editing.
- Stay inside the active batch's allowed paths.
- Keep each batch as a complete vertical slice with deterministic tests and visible learner value.
- Add or update schema fixtures when changing the course contract.
- Preserve backward compatibility or provide a versioned migration path.
- Every new interactive control must be keyboard-accessible and visibly labeled.
- Every plot must have units, axes/legends where applicable, and a text interpretation.
- Debounce interactive compute, cancel stale requests, and never let an old response overwrite a newer state.
- Run `./scripts/verify.sh` before declaring a batch complete.

## Content-adapter rules

- Legacy MATLAB course import is read-only and additive; do not rewrite source course repositories during discovery.
- The native module contract is `course.yaml` + `module.yaml` + optional `lesson.md` + an approved runtime entrypoint.
- A static module is valid and should not be forced to invent meaningless controls.
- Interactive modules should expose the smallest useful set of parameters and at least one interpretation-oriented failure or comparison when pedagogically appropriate.

## Portfolio Control alignment

- Intended product slug: `engineering-learning-platform`.
- Intended delivery profile: `product-data`.
- Human approval is required for protected-branch merge and production deployment.
- Required evidence includes schema validation, catalog completeness, deterministic numerical results, service smoke tests, migration/rollback notes, and visual/accessibility review.

<!-- BEGIN PORTFOLIO-CONTROL MANAGED -->
## Governed agentic delivery

- Product: `engineering-learning-platform`; delivery profile: `product-data`.
- Control revision: `789d2129f0137086a6ebd784cfb000b45a8ae978`; harness version: `2`.
- Read `contracts/profile-requirements.yaml` and the approved
  `contracts/active-batch.yaml` before implementation.
- Stay inside active-batch allowed paths and preserve every forbidden path.
- Run the repository-local verification contract before claiming completion.
- Record exact evidence and distinguish static, simulated, protocol, bench,
  field, playtest, staging, and production validation.
- Do not claim physical, release, deployment, or production evidence that was
  not actually produced.
<!-- END PORTFOLIO-CONTROL MANAGED -->
