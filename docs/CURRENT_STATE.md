# Current state

`ELP-DSP-FIDELITY-P21-P28` continues issue 441 from merged numerical replay repair
`b7e684d595bd777602c9aa22cd489189efa6584b`, authorized by control
`12ea755ee75f9fe7bc142f052362938d9cefb4c9`. Implementation and independent
scenario comparisons are complete. All mandatory local verification passed:
quick/full each passed 785 tests, plus source-attested DSP, contract, catalog,
lint, frontend typecheck/build, scope and API/live HTTP smoke checks.
[PR #46](https://github.com/tranquilWorks/engineering-learning-platform/pull/46)
is ready for review and awaits protected-merge approval. Hosted backend CI still
fails source/history checks because its checkout omits their prerequisites;
frontend CI passed at implementation revision `152ddf6`.

The eight lessons now expose AM envelope/coherent recovery, FM occupied bandwidth
and phase aliasing, energy-consistent BPSK/QPSK, explicit finite RRC pulses and
matched-filter delay, finite ZF/regularized multipath equalizers, changing-path
LMS, Wilson uncertainty from independent trials, and ROC/estimator selection bias.
Five named scenarios per lesson retain independent formulas and alternate
algorithms, with a declared absolute/relative signature tolerance of 1e-8.

P01 remains the distinct initial conversion; P02-P20 are prior repairs;
P21-P28 are current repairs; P29-P84 remain pending. All other module bytes,
source pins, source map and conversion manifest are unchanged. Only eight target
content digests change in coverage.yaml. Catalog remains six courses, 290 modules,
290 interactive experiments. Inventory does not imply course completion.

MATLAB, browser/accessibility, learner, physical/hardware, certification,
release/deployment and production verification remain unperformed.
