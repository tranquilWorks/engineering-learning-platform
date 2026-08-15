from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from fixture_course import (
    VALID_EXPERIMENT,
    make_read_only,
    make_writable,
    module_manifest,
    run_git,
    tree_snapshot,
    write_course,
)

from elp_api.catalog import CatalogError, CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError


def _python_module(*, blocks: list[dict] | None = None) -> dict:
    return module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        blocks=blocks if blocks is not None else [],
    )


def test_content_digest_is_repeatable_and_covers_only_validated_inputs(
    tmp_path: Path,
) -> None:
    course_dir = write_course(
        tmp_path,
        modules=[_python_module(blocks=[{"type": "markdown", "source": "lesson.md"}])],
        experiment=VALID_EXPERIMENT,
        lesson="# Initial lesson\n",
    )
    first = CourseCatalog([tmp_path])
    again = CourseCatalog([tmp_path])
    first_course = first.summaries()[0]
    first_module = first_course.modules[0]
    assert again.summaries()[0].revision == first_course.revision
    assert again.summaries()[0].modules[0].revision == first_module.revision
    assert first_course.revision.source_git_commit is None
    assert first_module.revision.source_git_commit is None

    (course_dir / "unreferenced.txt").write_text("not a contract input\n", encoding="utf-8")
    unrelated = CourseCatalog([tmp_path]).summaries()[0]
    assert unrelated.revision.content_digest == first_course.revision.content_digest

    lesson = next(course_dir.glob("modules/*/lesson.md"))
    lesson.write_text("# Changed lesson\n", encoding="utf-8")
    changed_lesson = CourseCatalog([tmp_path]).summaries()[0]
    assert changed_lesson.revision.content_digest != first_course.revision.content_digest
    assert changed_lesson.modules[0].revision.content_digest != first_module.revision.content_digest

    experiment = next(course_dir.glob("modules/*/experiment.py"))
    experiment.write_text(VALID_EXPERIMENT + "\n# reviewed change\n", encoding="utf-8")
    changed_runtime = CourseCatalog([tmp_path]).summaries()[0]
    assert (
        changed_runtime.modules[0].revision.content_digest
        != changed_lesson.modules[0].revision.content_digest
    )


def test_document_and_result_propagate_schema_content_git_and_runtime_identity(
    tmp_path: Path,
) -> None:
    write_course(tmp_path, modules=[_python_module()], experiment=VALID_EXPERIMENT)
    catalog = CourseCatalog([tmp_path])
    document = catalog.document("sample-course", "sample-module")
    result = ExperimentRuntime(catalog).run(
        "sample-course",
        "sample-module",
        {},
        expected_content_digest=document.module_revision.content_digest,
    )
    assert document.module.schema_version == 1
    assert document.course.revision.schema_version == 1
    assert result.course_revision == document.course.revision
    assert result.module_revision == document.module_revision
    assert result.module_revision.source_git_commit is None
    assert result.platform_revision.runtime_kind == "python-in-process"
    assert result.platform_revision.platform_version
    assert len(result.platform_revision.runtime_content_digest) == 64
    assert result.platform_revision == document.platform_revision


def test_catalog_and_runtime_do_not_write_a_read_only_course_tree(tmp_path: Path) -> None:
    course_dir = write_course(
        tmp_path,
        modules=[_python_module(blocks=[{"type": "plot", "plot": "main"}])],
        experiment=VALID_EXPERIMENT,
    )
    before = tree_snapshot(course_dir)
    make_read_only(course_dir)
    try:
        catalog = CourseCatalog([course_dir])
        document = catalog.document("sample-course", "sample-module")
        ExperimentRuntime(catalog).run(
            "sample-course",
            "sample-module",
            {},
            expected_content_digest=document.module_revision.content_digest,
        )
        after = tree_snapshot(course_dir)
        assert after == tuple(
            (name, 0o444 if digest != "dir" else 0o555, digest) for name, _, digest in before
        )
        assert not list(course_dir.rglob("__pycache__"))
        assert not list(course_dir.rglob("*.pyc"))
    finally:
        make_writable(course_dir)


def test_git_pin_recovers_last_reviewed_course_identity(tmp_path: Path) -> None:
    repository = write_course(tmp_path, modules=[_python_module()], experiment=VALID_EXPERIMENT)
    run_git(repository, "init", "-q")
    run_git(repository, "add", ".")
    run_git(repository, "commit", "-q", "-m", "reviewed v1")
    reviewed_commit = run_git(repository, "rev-parse", "HEAD")
    reviewed = CourseCatalog([repository]).summaries()[0]
    assert reviewed.revision.source_git_commit == reviewed_commit

    module_path = next(repository.glob("modules/*/module.yaml"))
    original = module_path.read_text(encoding="utf-8")
    module_path.write_text(
        original.replace("schema_version: 1", "schema_version: 2"), encoding="utf-8"
    )
    run_git(repository, "add", ".")
    run_git(repository, "commit", "-q", "-m", "unsupported future contract")
    future_commit = run_git(repository, "rev-parse", "HEAD")
    assert future_commit != reviewed_commit
    with pytest.raises(CatalogError, match="unsupported schema_version 2"):
        CourseCatalog([repository])

    run_git(repository, "switch", "-q", "--detach", reviewed_commit)
    recovered = CourseCatalog([repository]).summaries()[0]
    assert recovered.revision.source_git_commit == reviewed_commit
    assert recovered.revision.content_digest == reviewed.revision.content_digest


def test_generated_contracts_are_repeatable_and_drift_is_detected(tmp_path: Path) -> None:
    from scripts.export_schemas import drifted_paths, rendered_targets

    first = rendered_targets()
    second = rendered_targets()
    assert first == second
    assert drifted_paths(first) == []
    synthetic = tmp_path / "types.ts"
    synthetic.write_text("stale\n", encoding="utf-8")
    assert drifted_paths({synthetic: "generated\n"}) == [synthetic]
    for path, rendered in first.items():
        assert path.read_text(encoding="utf-8") == rendered


def test_accepted_snapshot_rejects_same_path_content_mutation(tmp_path: Path) -> None:
    course_dir = write_course(tmp_path, modules=[_python_module()], experiment=VALID_EXPERIMENT)
    catalog = CourseCatalog([tmp_path])
    document = catalog.document("sample-course", "sample-module")
    experiment = next(course_dir.glob("modules/*/experiment.py"))
    stat = experiment.stat()
    experiment.write_text(VALID_EXPERIMENT + "\n# same-mtime mutation\n", encoding="utf-8")
    os.utime(experiment, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    with pytest.raises(
        RuntimeContractError, match="accepted module input changed; reload required"
    ):
        ExperimentRuntime(catalog).run(
            "sample-course",
            "sample-module",
            {},
            expected_content_digest=document.module_revision.content_digest,
        )


def test_failed_reload_never_exposes_unvalidated_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    course_dir = write_course(tmp_path)
    catalog = CourseCatalog([tmp_path])
    accepted = catalog.summaries()
    module_path = next(course_dir.glob("modules/*/module.yaml"))
    module_path.write_text(
        "schema_version: 1\n"
        "id: rejected-module\n"
        "title: Rejected candidate\n"
        "status: implemented\n"
        "runtime:\n"
        "  kind: python\n"
        "  entrypoint: experiment.py:run\n",
        encoding="utf-8",
    )
    (module_path.parent / "experiment.py").write_text(
        "def run(parameters):\n    return {}\n", encoding="utf-8"
    )

    validation_started = threading.Event()
    release_validation = threading.Event()
    reader_started = threading.Event()
    reader_finished = threading.Event()

    def reject_candidate(*args: object, **kwargs: object) -> object:
        validation_started.set()
        assert release_validation.wait(timeout=2)
        raise RuntimeContractError("synthetic default rejection")

    def read_catalog() -> object:
        reader_started.set()
        try:
            return catalog.summaries()
        finally:
            reader_finished.set()

    monkeypatch.setattr(ExperimentRuntime, "run", reject_candidate)
    with ThreadPoolExecutor(max_workers=2) as executor:
        reload_future = executor.submit(catalog.reload)
        assert validation_started.wait(timeout=2)
        reader_future = executor.submit(read_catalog)
        assert reader_started.wait(timeout=2)
        assert not reader_finished.wait(timeout=0.1)
        release_validation.set()
        with pytest.raises(CatalogError, match="synthetic default rejection"):
            reload_future.result(timeout=2)
        assert reader_future.result(timeout=2) == accepted
