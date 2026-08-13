# Security Model

## Trust boundary

The platform executes only code checked into the platform repository or mounted from approved, read-only course repositories. It does not provide a browser code editor, arbitrary notebook execution, file upload execution, or dynamic dependency installation.

This is a **trusted-content runtime**, not a multi-tenant hostile-code sandbox.

## Foundation controls

- strict Pydantic manifest models with unknown fields rejected;
- stable control IDs and parameter allow-listing;
- path traversal prevention for lesson sources and Python entrypoints;
- runtime result-size limit;
- runtime timeout contract;
- deterministic default validation;
- no shell/subprocess interface exposed by the API;
- read-only production course mounts;
- unprivileged container user;
- read-only root filesystem in Compose;
- `no-new-privileges`;
- security response headers and same-origin production requests.

## Known limitation

Python threads cannot safely terminate malicious or deadlocked native code. The current timeout is an operational guard for trusted experiments, not a security sandbox. Before allowing untrusted authors, uploaded notebooks, or arbitrary learner code, execution must move to disposable worker processes/containers with:

- non-root UID;
- read-only root and course mount;
- empty writable scratch directory;
- no network by default;
- CPU, memory, process-count, and file-size limits;
- hard wall-clock termination;
- signed/allow-listed runtime images;
- queue-level concurrency limits;
- result-size enforcement outside the worker;
- audit trail binding content revision to execution.

## Corporate identity

Identity and access should initially be enforced by the existing corporate reverse proxy/ingress. A future identity adapter may consume signed identity context from that proxy. Never trust arbitrary user-supplied identity headers on a directly reachable application port.

## Data handling

Course parameters may eventually contain proprietary values. Production logging should record course/module identity, duration, outcome, and result size, but avoid raw parameter values by default. Course authors must not embed classified, export-controlled, personal, or otherwise restricted data without the corresponding accredited hosting boundary and review.

## Dependency and supply-chain controls

Recommended CI gates:

- lockfile integrity;
- npm and Python vulnerability scans;
- license inventory;
- secret scan;
- container vulnerability scan;
- SBOM generation;
- signed images;
- protected branch and human release approval.
