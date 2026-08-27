# ELP-ORG-IDENTITY evidence

## Identity and scope

- Target baseline: `923a86ab79893bd939d88d275bdcb12a5a1ddad6`
- Target baseline tree: `ebb16887a492d4327d0fbda4b58e933ed5645dfa`
- Merged control revision: `373aa5f5bd1ecc63740a03cba01c3eef237bb8af`
- Canonical control repository: `tranquilWorks/portfolio-control`
- Canonical target repository: `tranquilWorks/engineering-learning-platform`
- Canonical source owner: `tranquilWorks`
- Scope: repository identity and mechanically derived provenance only
- New or modified course content: none

All 13 source-course URLs in `.gitmodules` resolve under `tranquilWorks`.
A tracked-file audit reports zero remaining `kpbianco/` repository-owner
identities. GitHub redirects are not used as the canonical identity.

## Gitlink immutability

| Source course | Retained gitlink |
|---|---|
| Controls/GNC | `ffd6623ee2cf8ccd8599fffd935ef07370750fa3` |
| Distributed real-time | `97f455503e6d2ae65a87b31968bae4c32d2f7bc3` |
| DSP/Radar | `5d73667a486df4a7b6c581e4c9406e810ed4f0f6` |
| Embedded RT/HIL | `0ab836efcace36158687a467f64225bd5cff8177` |
| Flight dynamics | `131cc662845614d362133f685e0c159091001f76` |
| FPGA data path | `bf3d168ae4ab48ce4264d95f1b77a97a8d028f14` |
| HWIL systems | `94f12813572d0e4a0d3f30b4d143151a0066e074` |
| Numerical optimization | `4014f89fcfcdc18e037b4216cd42048f9adc400a` |
| Reliability/FDIR | `e604208c90c5424e6bd9dbcc22837b0fb2228c32` |
| RF lab | `5b1650d5ddc42757e14b27b112de1528ce0f7460` |
| Robotics/autonomy | `f8807640258f1a6c1c77f1dcc9e61734551c585b` |
| Statistics/estimation | `c5bc5ab6b723bfd9afd9039379628ceac3cff411` |
| Vehicle dynamics | `916c3e6a9cbbc9e1c4ede821e894132b13c3b9c8` |

`git diff --raw <baseline> -- courses/*-learning` is empty. Source commit,
tree, curriculum, and canonical-file hashes therefore remain unchanged.

## Provenance closure

| Artifact | Before transfer normalization | After |
|---|---|---|
| `.gitmodules` | `acbd5f8bfe9675bc25216b8494570dff4ceecd7f5553a60b4618db99f3ea442f` | `a2739650b61500f05b3331fa69f1a4c417f244b5aa55b06d25aac68fb352c792` |
| DSP source map | `dc46c37e2f1e8701127a504200c7a4fd9f84a9da5d7f2064474195eec7cb0e05` | `5b2751769cf70d7c4faad148fecd2db16e7995982122777fa012bfbda7850bf5` |
| DSP conversion manifest | `a6b7699ddb8b3a5b9e099fd382a555c3e7ea8345bb88fcdee4f054c1e636e193` | `1244c6dea11ea11b880e0f26d54ce81dea42ea1ab4981d4d5180c440eb7890a4` |
| DSP coverage ledger | prior retained ledger | `66ab0cb3dabda4a1b41f0aee1efcd1274ebfb854af1e145a7b43230b19bf8cba` |
| DSP authoring identity | `77b1d9497c085aad3fd2f3ff1f45113344420408f05893e4c23d2c68a7d64721` | `e4eb5b356791e480e82306c079961d91a4e4dc5cd1466fc23317a8915b32b8db` |
| GNC source map | `5004e2d35d592e398579dd075faa3d0fc7eba3c48579b838f73c1826aba32360` | `e274649c791d008254aab63a8036e6b7bef48720ec422f4cb0601f279347483c` |
| GNC conversion manifest | `173f65eeaf8d008b05d122a55cb90d02432296aa21a57086855f55af7aab95e7` | `02ddb580b164e7a52b7c6f18cb2dddd0837403bd238ea0d53e1dbc16967d3e7b` |
| GNC coverage ledger | prior retained ledger | `5e367f2431cf1dceb667cbf015c855d76edbff11fcbc3d6511a9544f54a58511` |

Every conversion record now binds the corresponding post-transfer source-map
digest. Framework validation proves all records, manifests, and ledgers close.

## Course-payload immutability

The baseline diff is empty for all:

- `course.yaml`
- `modules/*/module.yaml`
- `modules/*/lesson.md`
- `modules/*/experiment.py`
- `modules/*/evidence/**`

Generic API/UI/schema/runtime, dependencies, workflows, container/deployment
files, examples, and unfinished course gitlinks are unchanged. DSP/Radar
remains 84 converted; Controls/GNC remains 24 converted; both retain zero
pending, blocked, or placeholder entries.

## Local verification

| Check | Result |
|---|---|
| Combined DSP/GNC provenance frameworks | passed, 56 tests |
| Source-attested DSP/Radar suite | passed, 300 tests |
| Source-attested Controls/GNC suite | passed, 80 tests |
| Contract suite | passed, 72 tests |
| Quick backend suite | passed, 456 tests; 3 dependency deprecation warnings |
| Full verifier | passed; 4 courses / 110 modules / 110 interactive, backend 456 tests, frontend typecheck/build |
| Explicit deterministic catalog execution | passed; 4 / 110 / 110 |
| Ruff | passed |
| Diff whitespace check | passed after normalizing the imported contract EOF |
| Hosted backend/frontend/container | required on the exact final PR head |

## Claim boundary

This evidence establishes canonical `tranquilWorks` repository identity,
closed imported-course provenance, unchanged gitlinks/course payloads, and
unchanged deterministic software behavior. It adds no course or module.

MATLAB parity, learner effectiveness, browser/accessibility acceptance,
physical HIL/HWIL or timing, bench/field behavior, release, deployment,
credentials/settings, and production operation were not performed and are not
claimed.
