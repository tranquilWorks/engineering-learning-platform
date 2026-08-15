from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from fixture_course import (
    VALID_EXPERIMENT,
    course_manifest,
    module_manifest,
    write_course,
)
from pydantic import TypeAdapter, ValidationError

from elp_api.catalog import CatalogError, CourseCatalog
from elp_api.models import (
    CourseManifest,
    LessonBlock,
    ModuleManifest,
    PlotSpec,
    RunRequest,
)

INVALID_VERSIONS: tuple[tuple[str, Any], ...] = (
    ("missing", None),
    ("boolean", True),
    ("string", "1"),
    ("float", 1.0),
    ("zero", 0),
    ("negative", -1),
    ("future", 2),
)


@pytest.mark.parametrize(("name", "version"), INVALID_VERSIONS)
@pytest.mark.parametrize("model", [CourseManifest, ModuleManifest])
def test_manifests_accept_only_required_integer_v1(
    model: type[CourseManifest] | type[ModuleManifest], name: str, version: Any
) -> None:
    value = course_manifest() if model is CourseManifest else module_manifest()
    if name == "missing":
        value.pop("schema_version")
    else:
        value["schema_version"] = version
    with pytest.raises(ValidationError):
        model.model_validate(value)
    accepted = course_manifest() if model is CourseManifest else module_manifest()
    assert model.model_validate(accepted).schema_version == 1


@pytest.mark.parametrize(("name", "version"), INVALID_VERSIONS)
def test_catalog_course_version_diagnostics_are_file_and_version_aware(
    tmp_path: Path, name: str, version: Any
) -> None:
    value = course_manifest()
    if name == "missing":
        value.pop("schema_version")
    else:
        value["schema_version"] = version
    course_dir = write_course(tmp_path, course=value)
    expected = "'<missing>'" if name == "missing" else repr(version)
    with pytest.raises(
        CatalogError,
        match=rf"{course_dir / 'course.yaml'}: invalid CourseManifest schema_version={expected}",
    ):
        CourseCatalog([tmp_path])


@pytest.mark.parametrize(("name", "version"), INVALID_VERSIONS)
def test_catalog_module_version_diagnostics_are_file_and_version_aware(
    tmp_path: Path, name: str, version: Any
) -> None:
    value = module_manifest()
    if name == "missing":
        value.pop("schema_version")
    else:
        value["schema_version"] = version
    course_dir = write_course(tmp_path, modules=[value])
    module_path = next(course_dir.glob("modules/*/module.yaml"))
    expected = "'<missing>'" if name == "missing" else repr(version)
    with pytest.raises(
        CatalogError,
        match=rf"{module_path}: invalid ModuleManifest schema_version={expected}",
    ):
        CourseCatalog([tmp_path])


def test_malformed_and_duplicate_yaml_keys_fail_with_stable_paths(tmp_path: Path) -> None:
    course_dir = write_course(tmp_path)
    course_path = course_dir / "course.yaml"
    course_path.write_text(
        "schema_version: 1\nid: one\nid: two\ntitle: Duplicate\n", encoding="utf-8"
    )
    with pytest.raises(
        CatalogError, match=rf"(?s){course_path}: cannot read YAML: .*duplicate key"
    ):
        CourseCatalog([tmp_path])
    course_path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    with pytest.raises(CatalogError, match=rf"{course_path}: expected a YAML mapping"):
        CourseCatalog([tmp_path])
    course_path.write_text("? [not, hashable]\n: value\n", encoding="utf-8")
    with pytest.raises(
        CatalogError, match=rf"(?s){course_path}: cannot read YAML: .*unhashable key"
    ):
        CourseCatalog([tmp_path])


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.update({"unknown": True}),
        lambda value: value["runtime"].update({"unknown": "not-a-runtime-field"}),
        lambda value: value["controls"][0].update({"options": []}),
        lambda value: value["blocks"][0].update({"plot": "not-markdown"}),
        lambda value: value["blocks"][0]["props"].update({"unknown": True}),
    ],
    ids=["module", "runtime", "control-variant", "block-variant", "widget-props"],
)
def test_unknown_nested_manifest_structure_fails_closed(mutate: Any) -> None:
    base = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        controls=[
            {
                "id": "x",
                "type": "slider",
                "label": "X",
                "default": 1,
                "minimum": 0,
                "maximum": 2,
            },
            {
                "id": "y",
                "type": "number",
                "label": "Y",
                "default": 1,
                "minimum": 0,
                "maximum": 2,
            },
        ],
        blocks=[
            {
                "type": "widget",
                "widget": "parameter-map",
                "props": {
                    "x_control": "x",
                    "y_control": "y",
                    "x_label": "X (m)",
                    "y_label": "Y (s)",
                },
            }
        ],
    )
    mutate(base)
    with pytest.raises(ValidationError):
        ModuleManifest.model_validate(base)


def test_unknown_course_request_plot_shell_and_widget_id_fail_closed() -> None:
    with pytest.raises(ValidationError):
        CourseManifest.model_validate(course_manifest(unknown=True))
    with pytest.raises(ValidationError):
        RunRequest.model_validate(
            {
                "parameters": {},
                "expected_content_digest": "0" * 64,
                "unknown": True,
            }
        )
    with pytest.raises(ValidationError):
        PlotSpec.model_validate(
            {
                "data": [{"type": "scatter"}],
                "layout": {},
                "renderer_override": "unsafe",
            }
        )
    with pytest.raises(ValidationError, match="title or axis label"):
        PlotSpec.model_validate({"data": [{"type": "scatter"}], "layout": {}})
    with pytest.raises(ValidationError):
        TypeAdapter(LessonBlock).validate_python(
            {"type": "widget", "widget": "undeclared", "props": {}}
        )


def test_explicit_markdown_text_and_plotly_payload_carriers_remain_open() -> None:
    markdown = TypeAdapter(LessonBlock).validate_python(
        {
            "type": "markdown",
            "text": "# Arbitrary prose\n\n$E = mc^2$\n\n- custom content",
        }
    )
    assert markdown.type == "markdown"
    plot = PlotSpec.model_validate(
        {
            "data": [
                {
                    "type": "custom-plotly-trace",
                    "nested": {"arbitrary": [1, True, {"content": "allowed"}]},
                }
            ],
            "layout": {
                "title": "Generic labeled plot",
                "custom": {"renderer_payload": "allowed"},
            },
            "config": {"future_plotly_option": {"value": 3}},
        }
    )
    assert plot.layout["custom"] == {"renderer_payload": "allowed"}


@pytest.mark.parametrize(
    ("visible_when", "message"),
    [
        ({"missing": True}, "unknown controls"),
        ({"dependent": True}, "cannot reference its own"),
        ({"enabled": "yes"}, "must be boolean"),
        ({"level": 99}, "outside its range"),
        ({"mode": "invalid"}, "must match an option"),
    ],
)
def test_conditional_control_references_and_values_are_semantic(
    visible_when: dict[str, Any], message: str
) -> None:
    value = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        controls=[
            {"id": "enabled", "type": "toggle", "label": "Enabled", "default": True},
            {
                "id": "level",
                "type": "slider",
                "label": "Level",
                "default": 1,
                "minimum": 0,
                "maximum": 2,
            },
            {
                "id": "mode",
                "type": "select",
                "label": "Mode",
                "default": "a",
                "options": [{"label": "A", "value": "a"}],
            },
            {
                "id": "dependent",
                "type": "toggle",
                "label": "Dependent",
                "default": False,
                "visible_when": visible_when,
            },
        ],
    )
    with pytest.raises(ValidationError, match=message):
        ModuleManifest.model_validate(value)


def test_duplicate_module_id_and_number_fail_catalog_acceptance(tmp_path: Path) -> None:
    first = module_manifest(id="same", number=7)
    second = module_manifest(id="same", number=8)
    write_course(tmp_path, modules=[first, second])
    with pytest.raises(CatalogError, match="duplicate module ids"):
        CourseCatalog([tmp_path])

    second["id"] = "different"
    second["number"] = 7
    other = tmp_path / "other"
    write_course(other, modules=[first, second])
    with pytest.raises(CatalogError, match="duplicate module numbers"):
        CourseCatalog([other])


@pytest.mark.parametrize(
    ("blocks", "message"),
    [
        ([{"type": "plot", "plot": "missing"}], "missing plot"),
        ([{"type": "plot_grid", "plots": ["main", "missing"]}], "missing plots"),
        ([{"type": "table", "table": "missing"}], "missing table"),
        ([{"type": "callout", "source": "missing"}], "missing explanation"),
    ],
)
def test_declared_output_references_must_exist_before_acceptance(
    tmp_path: Path, blocks: list[dict[str, Any]], message: str
) -> None:
    module = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        blocks=blocks,
    )
    write_course(tmp_path, modules=[module], experiment=VALID_EXPERIMENT)
    with pytest.raises(CatalogError, match=message):
        CourseCatalog([tmp_path])


def test_all_declared_output_reference_kinds_accept_valid_defaults(tmp_path: Path) -> None:
    module = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        blocks=[
            {"type": "plot", "plot": "main"},
            {"type": "table", "table": "cases"},
            {"type": "callout", "source": "interpretation"},
        ],
    )
    write_course(tmp_path, modules=[module], experiment=VALID_EXPERIMENT)
    assert CourseCatalog([tmp_path]).summaries()[0].id == "sample-course"


def test_manifest_paths_cannot_escape_or_follow_symlinks(tmp_path: Path) -> None:
    write_course(tmp_path, course=course_manifest(modules_path="../outside"))
    with pytest.raises(CatalogError, match="modules_path escapes"):
        CourseCatalog([tmp_path])

    source_root = tmp_path / "source"
    course_dir = write_course(
        source_root,
        modules=[module_manifest(blocks=[{"type": "markdown", "source": "../outside.md"}])],
    )
    (course_dir / "modules" / "outside.md").write_text("outside", encoding="utf-8")
    with pytest.raises(CatalogError, match="markdown source must be a normalized relative path"):
        CourseCatalog([source_root])

    runtime_root = tmp_path / "runtime"
    write_course(
        runtime_root,
        modules=[
            module_manifest(
                status="implemented",
                runtime={"kind": "python", "entrypoint": "../outside.py:run"},
                blocks=[],
            )
        ],
    )
    with pytest.raises(CatalogError, match="runtime entrypoint must be a normalized relative path"):
        CourseCatalog([runtime_root])

    outside = write_course(tmp_path / "outside")
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "linked-course").symlink_to(outside, target_is_directory=True)
    with pytest.raises(CatalogError, match="course directory escapes collection root"):
        CourseCatalog([collection])


def test_duplicate_control_ids_and_parameter_map_contract_are_rejected() -> None:
    control = {
        "id": "x",
        "type": "slider",
        "label": "X",
        "default": 1,
        "minimum": 0,
        "maximum": 2,
    }
    with pytest.raises(ValidationError, match="control ids must be unique"):
        ModuleManifest.model_validate(
            module_manifest(
                status="implemented",
                runtime={"kind": "python", "entrypoint": "experiment.py:run"},
                controls=[deepcopy(control), deepcopy(control)],
            )
        )
    with pytest.raises(ValidationError, match="distinct controls"):
        ModuleManifest.model_validate(
            module_manifest(
                status="implemented",
                runtime={"kind": "python", "entrypoint": "experiment.py:run"},
                controls=[control],
                blocks=[
                    {
                        "type": "widget",
                        "widget": "parameter-map",
                        "props": {
                            "x_control": "x",
                            "y_control": "x",
                            "x_label": "X",
                            "y_label": "X again",
                        },
                    }
                ],
            )
        )
