from fastapi.testclient import TestClient

from elp_api.main import app


def test_health_and_vertical_slice() -> None:
    client = TestClient(app)
    assert client.get("/api/v1/health").json()["status"] == "ok"
    catalog = client.get("/api/v1/catalog")
    assert catalog.status_code == 200
    response = client.post(
        "/api/v1/courses/demo-radar/modules/30-measure-range-from-echo-delay/run",
        json={"parameters": {"sample_rate_mhz": 40}},
    )
    assert response.status_code == 200
    result = response.json()
    metrics = {metric["id"]: metric for metric in result["metrics"]}
    assert metrics["range_bin"]["value"] < 4


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
