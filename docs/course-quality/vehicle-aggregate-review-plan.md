# Vehicle aggregate qualification — working checkpoint

Owner authorized content-only completion, push and merge; Docker remains deferred. Batch ELP-VEHICLE-AGGREGATE-QUALITY-01; target baseline 9c27f567399cf2fcb9728fb104b2d573fcac5652; Control draft PR636 at 931837fd3a910def43ee3d19ce2d2850778fa4dd. Branch codex/vehicle-aggregate-quality-20261105. No aggregate acceptance yet.

Existing inventory: 67 lessons, 14 competency portfolios, P66 telemetry and P67 GR86 digital twin. Original source pins and conversion artifacts, other course payloads and generic platform code are protected. All 13 pinned submodules and full target history are available. Python .venv and npm dependencies installed. Use single-thread BLAS for checks.

Audit findings (pending verification):
- P26/34/35/52/53 plot axes combine unlike quantities; separate axes and identify scaling for mixed-state diagnostics.
- P33's residual-only band is not a full prediction interval; preserve historical component and add conditional parameter-uncertainty propagation with explicit deterministic-noise limitation.
- P36 characteristic-speed zero sentinel needs applicability and critical-speed interpretation.
- P37 static yaw-moment derivative is not full-state stability: add executed nonlinear bicycle trim/Jacobian/transient, with bounded validity and an independent trajectory solution.
- P38 transferred load T satisfies M=T*track but tire loads use W/2 +/- T/2. Correct factor two and explicitly bound wheel-contact domain.
- P39 mixes metres and radians in modal participation and physical residual norms. Use kinetic-energy fractions and mass-weighted residual/coupling; independent generalized eigenproblem.
- P45/47 time-to-target sentinels must be labeled censored; P47 torque interruptions incorrectly freeze speed instead of paying drag. P48 is a requested-deceleration conditional allocation, not a self-consistent achieved-load equilibrium.
- P49 target also controls synthetic force-curve peak; terminal low-speed floor and wheel-speed projection restrict stopping-distance and dynamics claims.
- P52/53/55 mixed-unit residuals need declared dimensionless scales; P54 known offset is applied, not inferred; P56 correction is a fixed-gain observer, not calibrated GPS fusion.
- P57 covariance recurrence omits plant propagation and observation-noise covariance; fix uncertainty mechanics or explicitly preserve old proxy separately. State scales must distinguish yaw rate from angles.
- P59 covariance via normal equations and two-truth containment are not empirical coverage. Use stable factorization and truthful conditional diagnostics.
- P60 recovery is deterministic fixture replay with known nominal lengths, not unknown live transport qualification.
- P66/P67 have substantial executed integration already. Audit full stage and requirement closure, independently check histories and limiting cases. No measured GR86, hardware, track or safety claim.

Remaining: finish audit, repair models/references, author 67 unique checkpoints and worked derivations plus 14 portfolios, preserve prior assessment prose and manifest identities; refresh only current target identities and explicitly changed native evidence. Replay 335 cases both runtime and real HTTP, 134 browser views/interactions, 28 portfolio visits; inspect plots/math, run frontend/browser regressions and frozen contract/quick/full. Promote only after all nine review dimensions pass, archive precise evidence, push and merge target and Control. Do not mistake this checkpoint for completion.

## Implemented checkpoint (2026-11-05)

- Authored 67 distinct checkpoint tasks with worked reasoning and limitations, plus 14 individually specified integration portfolios. Generator preserves all 16 prior assessment tasks verbatim and all prior controls/blocks. JSON source manifests remain JSON for existing consumers.
- P37 now executes a bounded nonlinear bicycle trim, analytic full-state Jacobian, RK4 transient, domain cutoff and force utilization; independent lateral-velocity DOP853 histories, finite perturbations and step refinement pass. P38 corrects transferred-load factor two and reports contact-domain excess. P39 uses kinetic-energy fractions and mass-weighted residuals with independent generalized eigenvectors.
- P33 adds conditional predictive variance while labeling historical residual containment honestly. P57 uses complete fixed-gain Joseph covariance with plant propagation and measurement noise; independent finite covariance sums compare the full history. P59 uses SVD covariance with QR reference and labels two-parameter containment honestly. P47 now decelerates under resistance during torque interruption. Mixed axes corrected in P26/34/35/52/53; characteristic/critical-speed applicability and target-time censor flags added.
- **31 focused mechanism tests passed**. Initial test caught a misplaced metric tuple in the P45/P47 result comprehension; repaired before the passing rerun. First aggregate replay exposed missing optional relative tolerance on P17–24 and absent evidence directories; repaired without widening the original absolute budget.
- **335 independent runtime comparisons passed** across all 67 lessons. P01–16 additionally compare every previously independent physical/response field. Changed P38/39/47/57/59 native golden files retain pre-aggregate copies. Current bindings are in vehicle-aggregate-replay.json; they must be refreshed if learner-facing content changes.
- Chromium headless shell installed through Playwright 1.56.1 fallback. Browser/HTTP review has not yet run. Broader Vehicle tests are running in .state/vehicle/aggregate-initial.log; resolve actual results before claiming acceptance. Historical aggregate guards now recognize this exact successor; new Vehicle guard protects all other courses and original P01–24 runtime/lesson/verification bytes.

Still pending: finish capstone/history and off-grid audit, verify new assessment accuracy, check all manifests and current coverage identities, actual browser/HTTP + plot/math review, audit projection, frozen contract/quick/full, maturity evidence, target/Control push and merge. No aggregate acceptance or merge yet.
