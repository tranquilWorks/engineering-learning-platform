from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, ORJSONResponse

from .catalog import CatalogError, CourseCatalog
from .config import Settings
from .models import RunRequest
from .runtime import ExperimentRuntime, RuntimeContractError, RuntimeTimeout

settings = Settings.from_env()
catalog = CourseCatalog(settings.course_paths)
runtime = ExperimentRuntime(catalog, default_timeout=settings.runtime_timeout_seconds)

app = FastAPI(
    title="Engineering Learning Platform API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)

if settings.dev_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.dev_cors),
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Accept"],
    )


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; connect-src 'self'; font-src 'self' data:; "
        "worker-src 'self' blob:",
    )
    return response


@app.get("/api/v1/health")
def health() -> dict[str, object]:
    return {"status": "ok", "courses": len(catalog.summaries())}


@app.post("/api/v1/admin/reload")
def reload_catalog() -> dict[str, object]:
    try:
        catalog.reload()
    except CatalogError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"status": "reloaded", "courses": len(catalog.summaries())}


@app.get("/api/v1/catalog")
def get_catalog():
    return catalog.summaries()


@app.get("/api/v1/courses/{course_id}")
def get_course(course_id: str):
    try:
        return catalog.course(course_id).summary()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/courses/{course_id}/assets/{asset_path:path}", include_in_schema=False)
def get_course_asset(course_id: str, asset_path: str):
    try:
        return FileResponse(catalog.course_asset(course_id, asset_path))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get(
    "/api/v1/courses/{course_id}/modules/{module_id}/assets/{asset_path:path}",
    include_in_schema=False,
)
def get_module_asset(course_id: str, module_id: str, asset_path: str):
    try:
        return FileResponse(catalog.module_asset(course_id, module_id, asset_path))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/courses/{course_id}/modules/{module_id}")
def get_module(course_id: str, module_id: str):
    try:
        return catalog.document(course_id, module_id)
    except (KeyError, CatalogError, OSError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/v1/courses/{course_id}/modules/{module_id}/run")
def run_module(course_id: str, module_id: str, request: RunRequest):
    try:
        result = runtime.run(
            course_id,
            module_id,
            request.parameters,
            expected_content_digest=request.expected_content_digest,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeTimeout as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except RuntimeContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    encoded = json.dumps(result.model_dump(mode="json"), separators=(",", ":")).encode("utf-8")
    if len(encoded) > settings.max_result_bytes:
        raise HTTPException(
            status_code=413,
            detail="result exceeds inline JSON limit; use the planned Arrow artifact path",
        )
    return result


def _web_file(path: str) -> FileResponse:
    assert settings.web_dist is not None
    requested = (settings.web_dist / path).resolve()
    if settings.web_dist not in requested.parents and requested != settings.web_dist:
        raise HTTPException(status_code=404)
    if requested.is_file():
        return FileResponse(requested)
    index = settings.web_dist / "index.html"
    if index.is_file():
        return FileResponse(index)
    raise HTTPException(status_code=404)


if settings.web_dist and settings.web_dist.is_dir():

    @app.get("/{path:path}", include_in_schema=False)
    def web(path: str):
        return _web_file(path or "index.html")
