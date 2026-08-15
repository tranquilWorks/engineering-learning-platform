from dataclasses import replace

from fastapi.testclient import TestClient

import elp_api.main as main_module
from elp_api.main import app


def test_health_and_vertical_slice() -> None:
    client = TestClient(app)
    assert client.get("/api/v1/health").json()["status"] == "ok"
    catalog = client.get("/api/v1/catalog")
    assert catalog.status_code == 200
    radar = next(item for item in catalog.json() if item["id"] == "demo-radar")
    module_revision = radar["modules"][0]["revision"]
    response = client.post(
        "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/run",
        json={
            "parameters": {"sample_rate_mhz": 40},
            "expected_content_digest": module_revision["content_digest"],
        },
    )
    assert response.status_code == 200
    result = response.json()
    metrics = {metric["id"]: metric for metric in result["metrics"]}
    assert metrics["range_bin"]["value"] < 4
    assert result["module_revision"] == module_revision
    assert result["course_revision"] == radar["revision"]
    assert len(result["platform_revision"]["runtime_content_digest"]) == 64


def test_module_asset_is_served_and_traversal_is_rejected() -> None:
    client = TestClient(app)
    asset = client.get(
        "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/assets/range-geometry.svg"
    )
    assert asset.status_code == 200
    assert "svg" in asset.headers["content-type"]
    traversal = client.get(
        "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/assets/../experiment.py"
    )
    assert traversal.status_code == 404


def test_run_request_is_strict_and_requires_content_revision() -> None:
    client = TestClient(app)
    path = "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/run"
    assert client.post(path, json={"parameters": {}}).status_code == 422
    assert (
        client.post(
            path,
            json={
                "parameters": {},
                "expected_content_digest": "0" * 64,
                "unknown": True,
            },
        ).status_code
        == 422
    )


def test_stale_revision_and_inline_result_size_fail_closed(monkeypatch) -> None:
    client = TestClient(app)
    path = "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/run"
    stale = client.post(
        path,
        json={"parameters": {}, "expected_content_digest": "0" * 64},
    )
    assert stale.status_code == 422
    assert "stale" in stale.json()["detail"]

    catalog = client.get("/api/v1/catalog").json()
    radar = next(item for item in catalog if item["id"] == "demo-radar")
    digest = radar["modules"][0]["revision"]["content_digest"]
    monkeypatch.setattr(
        main_module,
        "settings",
        replace(main_module.settings, max_result_bytes=128),
    )
    oversized = client.post(
        path,
        json={"parameters": {}, "expected_content_digest": digest},
    )
    assert oversized.status_code == 413
