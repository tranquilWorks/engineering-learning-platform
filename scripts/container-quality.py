#!/usr/bin/env python3
"""Exercise every baked lesson through HTTP; retain bounded per-lesson evidence."""

import hashlib
import json
import os
import subprocess
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.environ.get("ELP_BROWSER_URL", "http://127.0.0.1:8767")
NAME = os.environ.get("ELP_CONTAINER_NAME", "elp-course-quality")
OUT = Path("docs/course-quality/container-report.json")


def call(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    with urlopen(
        Request(BASE + path, data=data, headers={"Content-Type": "application/json"}),
        timeout=60,
    ) as response:
        raw = response.read(8388609)
        assert len(raw) <= 8388608, "Result exceeds configured bound"
        return json.loads(
            raw, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value))
        ), len(raw)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, allow_nan=False).encode()
    ).hexdigest()


def main():
    info = json.loads(subprocess.check_output(["docker", "inspect", NAME]))[0]
    assert info["Config"]["User"] == "65532:65532"
    assert info["HostConfig"]["ReadonlyRootfs"]
    assert info["HostConfig"]["Tmpfs"]["/tmp"].endswith("size=128m")
    assert info["NetworkSettings"]["Ports"] == {
        "8080/tcp": [{"HostIp": "127.0.0.1", "HostPort": BASE.rsplit(":", 1)[1]}]
    }
    assert not [m for m in info["Mounts"] if m.get("RW") and m["Destination"] != "/tmp"]
    for variable in [
        "OPENBLAS_NUM_THREADS=1",
        "OMP_NUM_THREADS=1",
        "MKL_NUM_THREADS=1",
    ]:
        assert variable in info["Config"]["Env"]
    write = subprocess.run(
        [
            "docker",
            "exec",
            NAME,
            "python",
            "-c",
            "from pathlib import Path; Path('/app/courses/write-probe').write_text('probe')",
        ],
        capture_output=True,
        check=False,
    )
    assert write.returncode != 0 and b"Read-only file system" in write.stderr
    catalog, _ = call("/api/v1/catalog")
    assert len(catalog) == 6 and sum(len(c["modules"]) for c in catalog) == 290
    rows = []
    report = {
        "validation_level": "local_readonly_nonroot_container_real_http",
        "image": info["Image"],
        "base": BASE,
        "readonly_write_rejected": True,
        "course_count": 6,
        "rows": rows,
        "production_deployment": "not_run",
    }
    for course in catalog:
        for module in course["modules"]:
            row = {"course": course["id"], "module": module["id"], "status": "failed"}
            try:
                path = f"/api/v1/courses/{course['id']}/modules/{module['id']}"
                doc, _ = call(path)
                payload = {
                    "parameters": doc["default_parameters"],
                    "expected_content_digest": doc["module_revision"]["content_digest"],
                }
                result, size = call(path + "/run", payload)
                repeat, _ = call(path + "/run", payload)
                assert digest(result) == digest(repeat), "Non-deterministic result"
                assert result["module_revision"] == doc["module_revision"]
                assert result["metrics"] and result["plots"]
                row.update(
                    result_bytes=size,
                    result_sha256=digest(result),
                    content_digest=doc["module_revision"]["content_digest"],
                    metric_count=len(result["metrics"]),
                    plot_count=len(result["plots"]),
                )
                try:
                    call(
                        path + "/run", {**payload, "expected_content_digest": "0" * 64}
                    )
                    raise AssertionError("Stale digest accepted")
                except HTTPError as error:
                    assert error.code == 422
                row["stale_digest_rejected"] = True
                if "broken_mode" in payload["parameters"]:
                    broken, _ = call(
                        path + "/run",
                        {
                            **payload,
                            "parameters": {
                                **payload["parameters"],
                                "broken_mode": True,
                            },
                        },
                    )
                    recovered, _ = call(path + "/run", payload)
                    assert digest(broken) != digest(result) and digest(
                        recovered
                    ) == digest(result)
                    row["failure_recovery"] = "passed"
                else:
                    row["failure_recovery"] = "not_declared"
                with urlopen(BASE + path.removeprefix("/api/v1")) as response:
                    html = response.read().decode()
                    assert '<div id="root">' in html and "/assets/" in html
                row["status"] = "passed"
            except (AssertionError, OSError, ValueError, KeyError) as error:
                row["failure"] = str(error)
            rows.append(row)
            OUT.write_text(json.dumps(report, indent=2) + "\n")
            print(len(rows), course["id"], module["id"], row["status"], flush=True)
    # Fetch the actual hashed entry asset, not only the SPA fallback.
    import re

    asset = re.search(r'src="([^"]+\.js)"', html).group(1)
    with urlopen(BASE + asset) as response:
        assert (
            "javascript" in response.headers["Content-Type"]
            and len(response.read()) > 1000
        )
    report["static_asset_verified"] = asset
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    assert all(row["status"] == "passed" for row in rows)


if __name__ == "__main__":
    main()
