# Revised-course delivery quality evidence

## Identity and scope

Batch `ELP-COURSE-DELIVERY-QUALITY-01` starts from merged PR51,
`b8d760e6721ae0b94aaa503f4ca1599592266442`, tree
`83ace6b519c971b6fc295223c67b1e1f1c541779`. Control PR531 merged
as `54f37f75af557b36037ec61d04caa2b14e9b764e`; numeric menu amendment
PR532 merged as `bd18c4dd65a710c3c09d42aa92d169e63034aea3`.

All course payloads, thirteen source pins, source maps, numerical references,
public schema shape and hosted workflows are preserved. The native catalog
contains DSP84, Controls68, Robotics69, Vehicle67 and two examples: six courses,
290 interactive modules. Nine other pinned repositories remain source-only.

## Demonstrated defects repaired

- Source TeX delimiters previously rendered literally. Code-safe normalization
  now renders inline/display equations; legacy text subscripts and pseudoinverse
  notation render without KaTeX errors. Wide equations support keyboard scrolling.
- Closed mobile navigation previously retained focusable offscreen buttons.
  Navigation now hides/inerts the closed sidebar, manages focus and Escape,
  traps mobile navigation focus and names landmarks. GFM task lists have labels.
  Scrollable lesson code, Markdown/data tables and plot-range tables are keyboard
  focusable; the DSP P58 regression verifies actual Arrow-key scrolling.
- Long inline code expressions and metric names now wrap within mobile pages;
  the regression opens numeric ranges on three previously overflowing lessons.
- Navigation could retain prediction state and delayed responses from another
  lesson. Module identity, abort handling and stale digest rejection are checked.
- Browser JSON erased the distinction between integer and float menu choices,
  causing DSP P17–P20 to fail despite Python HTTP checks. Numeric equality now
  resolves to the declared value/type; booleans, strings and undeclared values
  remain rejected. Nonfinite and ambiguous numeric menu declarations fail early.
- Plotly 3 silently omitted legacy string-valued axis and colorbar titles.
  The generic renderer now adapts title strings to `title.text`, preserving
  authored units and course payloads. A real DSP P11/P70 regression checks
  primary/secondary axis and heatmap colorbar labels. The all-page sweep
  reconciles authored titles with resolved chart titles. See the
  [upstream migration rule](https://plotly.com/javascript/guides/migrating-to-v3/).
- Revision details are collapsed; lesson section links, plot names and numeric
  range tables improve navigation and inspection. A range table is not a full
  nonvisual curve description.

## Verification

| Gate | Retained result |
| --- | --- |
| Contract verification | 103 passed, 93.09 s |
| Quick backend verification | 1,265 passed, 3 existing FastAPI/Starlette deprecation warnings, 1,178.64 s |
| Full repository verification | 1,265 backend passed, 3 existing warnings, 1,124.48 s; schema, compile, deterministic catalog, frontend typecheck/build passed |
| Focused numeric runtime/manifest boundary | 94 passed, 59.73 s |
| Frontend tests | 9 passed, including rendering every native lesson and preserving plot titles |
| Focused actual Chromium regressions | 10 passed, 37.4 s |
| Actual read-only container HTTP | All 290 defaults, deterministic repeats, declared failure/recovery, stale-digest rejection, deep/static routes and bounded results passed |
| All-page desktop/mobile browser | 580/580 passed in Chromium 153.0.8010.12; 0 automated accessibility findings; 12 representative interaction checks and 12 hashed screenshots |

Actual image:
`sha256:21e887a86efffb32f936efdb4c1d3dbce2d8b1f780f4dd432ab4d096a1e527e2`.
The image runs as uid65532 with a read-only root/course filesystem, bounded
128 MiB temporary storage, numerical library threads limited to one and one
localhost port. The check attempts and rejects a root/course write. This is
local trusted-code delivery evidence, not hostile-code isolation or deployment.

Reproduce with the commands in `contracts/verification.yaml` and
`./scripts/verify-course-delivery.sh` with Node 22.12 or newer. The verifier uses pinned Playwright/axe,
installs its Chromium revision, builds the actual image and stops its own
container. Host Chromium system libraries are a prerequisite. The JSON reports
retain each lesson's content digest, viewport/check results, image identity and
screenshot hashes. Agent visual review of five retained desktop/mobile screenshots is recorded
in `docs/course-quality/visual-review.json` with the same image identity and
individual hashes. It confirms equation rendering, readable layout and visible
review notes; it does not establish learner effectiveness.

Hosted CI is separately reported on the PR and remains nonmandatory under the
retained owner direction. The predecessor PR51 hosted backend had 66 known
source/history checkout failures and 1,165 passes; frontend passed and container
was skipped. Those results are not claimed as green or as this batch's gates.

## Content findings and remaining sequence

Browser execution is not educational acceptance. The initially scoped direct inspection found twelve
content defects: Controls P66–68 use unexecuted capstone surrogates, Robotics
P68–69 use fixed replay/recovery verdicts, Vehicle P61–65 have dimensional and
performance defects, and Vehicle P66–67 have unexecuted cumulative chains.
The affected lessons display their specific limitation. All four aggregate
numerical/curriculum/capstone statuses remain blocked pending the corresponding
reviews. Existing item evidence is retained without implying semantic acceptance.

The next authorized scoped batch repairs these twelve existing lessons using
executed models, independently originated checks and concrete teaching material.
A separate DSP aggregate competency/cumulative-assessment batch follows. See
`docs/course-quality/semantic-repair-plan.md`; it is design, not repair evidence.

Manual screen-reader testing, representative learner effectiveness, MATLAB
execution, measured vehicle/track, hardware/HIL and production deployment remain
`not_run`. Rollback is a revert to the baseline, with no data/schema migration.
Numeric authoring validation now rejects duplicate `1`/`1.0` options; the current
catalog contains no such aliases.

Wider direct inspection then found 60 additional unsupported mechanisms or
mislabeled evidence in Controls/Robotics/Vehicle, bringing the register to 72 affected
lessons. Each is documented in `additional-semantic-findings.md` and the embedded
lesson projection. The initial twelve-lesson repair is not a closure of those
additional findings. The ledger/projection tests were rerun after expanding the
register; production backend and course payloads remained unchanged.

PR52 implementation head `71a6fd47abace6463efead59a56c4aeae4c12fe5` hosted
run `36465358235`: frontend passed; backend had **67 failures and 1,198 passes**
in 585.87 s, and the hosted container job was skipped. The 65 source-identity
failures lack the DSP source checkout; two history assertions lack the named
baseline/terminal commits in the shallow checkout. The new course-immutability
assertion accounts for one of those history failures. The actual job log was
inspected; these results are not claimed as hosted success. Local source/history
checks pass with the retained checkout. Workflows and test guarantees are unchanged.

The subsequent implementation head `013451d0bd6c20673494a81252d96afe7d9d153b`
hosted run `36467123121` had the same classified 67 backend failures and
1,198 passes (930.95 s); frontend passed, container skipped. The raw job log
was inspected. Later local frontend changes receive fresh browser/image checks.

Concurrent-load limitation: six simultaneous lesson pages on the two-CPU container
produced an observed three-second runtime deadline miss in DSP P26, despite its
passing sequential HTTP check. The retained `browser-load-observation.json`
records that failure. The final delivery driver paces actual experiment requests
one at a time while inspecting pages in parallel; it changes neither request
parameters nor server responses or runtime deadlines. Concurrent-user capacity
is not certified by the delivery sweep.

Final artifact reconciliation confirms one desktop and one mobile row for each
of the 290 container modules, matching content digests and all screenshot hashes.
Course payload/source-pin and active-contract scope checks passed. This PR’s
revision retains these reports; later course batches may regenerate the current
report paths without changing this historical verification.
