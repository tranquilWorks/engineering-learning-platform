# Deployment

## Local development

Prerequisites:

- Node.js 22 LTS or newer;
- npm;
- Python 3.12 or newer;
- API dependencies from `apps/api/pyproject.toml`.

```bash
npm install
python3 -m venv apps/api/.venv
apps/api/.venv/bin/pip install -e 'apps/api[dev]'
npm run dev
```

The UI listens on `5173`; the API listens on `8000`; Vite proxies `/api`.

## Single-port container

```bash
docker compose up --build
```

Browse to `http://localhost:8080`.

The production image:

1. builds the Vite application;
2. installs the FastAPI package;
3. copies built-in courses;
4. runs as an unprivileged user;
5. serves the API and SPA on one port.

The Compose example mounts `./courses` read-only, runs with a read-only root filesystem, uses a bounded tmpfs, and enables `no-new-privileges`.

## Mount independent course repositories

```yaml
services:
  learning-platform:
    environment:
      ELP_COURSE_PATHS: /app/courses:/courses/dsp-radar:/courses/controls
    volumes:
      - ./courses:/app/courses:ro
      - ../dsp-radar_learning:/courses/dsp-radar:ro
      - ../controls-gnc-learning:/courses/controls:ro
```

A legacy course will not appear until it contains a native `course.yaml` at the mounted root or one directory beneath it. The platform does not mutate mounted source repositories.

## Corporate network pattern

Recommended deployment:

```text
corporate DNS
    │
HTTPS ingress / reverse proxy
    ├── SSO and authorization
    ├── TLS termination
    ├── request/body limits
    └── audit logging
            │
            ▼
ELP container :8080
    ├── read-only course mounts
    └── no direct internet requirement
```

Use the corporation's established identity gateway rather than implementing a second password store. Keep the application inaccessible except through the trusted proxy until identity-header validation is implemented.

## Configuration

| Variable | Default | Purpose |
|---|---:|---|
| `ELP_COURSE_PATHS` | `./courses` | Path-separated course roots |
| `ELP_WEB_DIST` | unset | Compiled SPA directory; unset in API-only development |
| `ELP_DEV_CORS` | `http://localhost:5173` | Development browser origins |
| `ELP_RUNTIME_TIMEOUT_SECONDS` | `5` | Default trusted experiment timeout |
| `ELP_MAX_RESULT_BYTES` | `8388608` | Maximum inline JSON response |

## Air-gapped/offline deployment

For a network without external package access:

1. resolve and lock dependencies in an approved connected build environment;
2. mirror npm and Python packages into the corporate artifact repository;
3. build the image in CI from those mirrors;
4. export/sign/scan the image;
5. import it into the internal registry;
6. mount approved course revisions read-only.

Do not perform runtime package installation.

## Kubernetes/OpenShift

Do not require Kubernetes for the first deployment. A single VM/container host is sufficient for a modest internal audience. When using existing Kubernetes/OpenShift infrastructure:

- run at least two API replicas only after experiment execution is stateless;
- use readiness/liveness probes on `/api/v1/health`;
- set CPU/memory requests and limits;
- mount course content from immutable images or read-only volumes;
- use ingress SSO/TLS;
- move heavy execution to separate workers before autoscaling the web tier.

## Upgrade and rollback

- Course schemas are versioned.
- Build images with immutable tags containing the Git SHA.
- Keep the previous image and course-content revision deployable.
- Run `scripts/validate_courses.py --execute --deterministic` before promotion.
- Roll back application and course revision together when a contract change spans both.
