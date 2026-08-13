# ADR 0001: React, FastAPI, and Plotly JSON

## Status

Accepted for the foundation.

## Context

The product needs an experience close to an interactive in-chat learning block while running independently on a corporate port. It must support broad numerical plotting, reactive controls, ordinary course folders, and a Python scientific-computing ecosystem.

## Decision

- React + TypeScript + Vite for the learner interface.
- FastAPI for catalog, runtime, and single-port static serving.
- Plotly figure JSON as the initial visualization interchange.
- NumPy/SciPy/pandas trusted Python functions as the initial runtime.
- Course folders and versioned manifests as canonical content inputs.

## Consequences

Positive:

- professional custom UX rather than notebook chrome;
- broad plotting coverage, including 3-D and engineering-specific traces;
- Python scientific stack integrates naturally;
- one output contract can later serve MATLAB, GPU, remote, and WASM adapters;
- frontend and course content remain independently testable.

Negative:

- more platform code than a notebook-only approach;
- Plotly bundle is large;
- Python runtime requires isolation before hostile/untrusted execution;
- course authors must explicitly map MATLAB outputs into the native result envelope.
