# Handoff

Do not run target-owned commands or modify product/course content while `ELP-G-ONBOARDING-HOLD` is active. Complete the Portfolio Control pointer PR, synchronize clean `main` checkouts, and run only the control-owned `ELP-G-PLAN-BASELINE` structural verifier. The harness control revision stays pinned until that gate succeeds.

A later human-reviewed contract must replace the hold before implementation or the commands in `contracts/verification.yaml` may run.
