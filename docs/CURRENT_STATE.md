# Current state

ELP-B010-01 is merged on `main`, and its exact-head GitHub Actions verification
passed. Main commit `8019d1798ea771f1f466e24c9983549ec1d6c127` is the audited
baseline for ELP-DSP-00.

ELP-DSP-00 implementation is in progress. It pins the read-only canonical
DSP/Radar source at commit `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`
and establishes a platform-owned conversion framework. The framework state is
`pending=84`, `converted=0`, `blocked=0`, and `placeholder=0`. No native DSP
learner module, Python experiment, or converted lesson is claimed by this
batch.

The current framework catalog contains three courses, two implemented modules,
and two interactive modules. The DSP course is the third course but currently
has zero modules; its presence proves discovery of the empty native course,
not 84 visible lessons or learner readiness.

The conversion lane is sequential and one item per batch:
`ELP-DSP-P01` through `ELP-DSP-P84`, followed by the aggregate
`ELP-DSP-G-PYTHON` gate. P01 is the first pending item; later items cannot skip
ahead.

ELP-DSP-00 remains a candidate until its exact PR head passes the required
hosted jobs and the governed merge completes. A branch, commit, pull request, or
green build alone is not merge, release, deployment, or production evidence.
Consult the retained ELP-DSP-00 evidence record for the exact candidate and
hosted-CI state rather than inferring it from this current-state summary.
