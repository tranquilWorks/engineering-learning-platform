from __future__ import annotations

import math
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

SCHEMA_VERSION = 1
SchemaVersion = Literal[1]
NonEmptyString = Annotated[str, Field(min_length=1)]
ResultKey = Annotated[str, Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
GitCommit = Annotated[str, Field(pattern=r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")]
Scalar = str | int | float | bool | None


def _exact_schema_version(value: Any) -> Any:
    if type(value) is not int:
        raise ValueError("schema_version must be the integer 1")
    if value != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version {value}; expected {SCHEMA_VERSION}")
    return value


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        json_schema_serialization_defaults_required=True,
    )


class CourseManifest(StrictModel):
    schema_version: SchemaVersion
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    title: NonEmptyString
    description: str = ""
    order: int = 0
    modules_path: NonEmptyString = "modules"
    tags: list[NonEmptyString] = Field(default_factory=list)

    _validate_schema_version = field_validator("schema_version", mode="before")(
        _exact_schema_version
    )


class ControlOption(StrictModel):
    label: NonEmptyString
    value: str | int | float | bool


class ControlBase(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: NonEmptyString
    description: NonEmptyString | None = None
    unit: NonEmptyString | None = None
    visible_when: dict[str, Scalar] | None = None


class NumericControlBase(ControlBase):
    default: int | float
    minimum: float
    maximum: float
    step: float | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_range(self) -> NumericControlBase:
        values = (float(self.default), self.minimum, self.maximum)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("numeric control values must be finite")
        if self.minimum >= self.maximum:
            raise ValueError("numeric control minimum must be below maximum")
        if not self.minimum <= float(self.default) <= self.maximum:
            raise ValueError("numeric control default must be inside its range")
        return self


class SliderControl(NumericControlBase):
    type: Literal["slider"]


class NumberControl(NumericControlBase):
    type: Literal["number"]


class ToggleControl(ControlBase):
    type: Literal["toggle"]
    default: bool


class SelectControl(ControlBase):
    type: Literal["select"]
    default: str | int | float | bool
    options: list[ControlOption] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_default(self) -> SelectControl:
        rendered = [(type(option.value).__name__, option.value) for option in self.options]
        if len(rendered) != len(set(rendered)):
            raise ValueError("select control option values must be unique")
        if len({str(option.value) for option in self.options}) != len(self.options):
            raise ValueError("select control option values must have unique text forms")
        if not any(
            type(self.default) is type(option.value) and self.default == option.value
            for option in self.options
        ):
            raise ValueError("select control default must match one option")
        return self


class SegmentedControl(ControlBase):
    type: Literal["segmented"]
    default: str | int | float | bool
    options: list[ControlOption] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_default(self) -> SegmentedControl:
        rendered = [(type(option.value).__name__, option.value) for option in self.options]
        if len(rendered) != len(set(rendered)):
            raise ValueError("segmented control option values must be unique")
        if len({str(option.value) for option in self.options}) != len(self.options):
            raise ValueError("segmented control option values must have unique text forms")
        if not any(
            type(self.default) is type(option.value) and self.default == option.value
            for option in self.options
        ):
            raise ValueError("segmented control default must match one option")
        return self


class ButtonControl(ControlBase):
    type: Literal["button"]
    default: Scalar = None


ControlSpec = Annotated[
    SliderControl
    | NumberControl
    | ToggleControl
    | SelectControl
    | SegmentedControl
    | ButtonControl,
    Field(discriminator="type"),
]


class StaticRuntime(StrictModel):
    kind: Literal["static"] = "static"
    trust: Literal["local-trusted"] = "local-trusted"


class PythonRuntime(StrictModel):
    kind: Literal["python"]
    entrypoint: NonEmptyString
    trust: Literal["local-trusted"] = "local-trusted"
    timeout_seconds: float | None = Field(default=None, gt=0, le=60)


RuntimeSpec = Annotated[StaticRuntime | PythonRuntime, Field(discriminator="kind")]


class TitledBlock(StrictModel):
    title: NonEmptyString | None = None


class MarkdownBlock(TitledBlock):
    type: Literal["markdown"]
    source: NonEmptyString | None = None
    text: NonEmptyString | None = None

    @model_validator(mode="after")
    def validate_content(self) -> MarkdownBlock:
        if (self.source is None) == (self.text is None):
            raise ValueError("markdown block requires exactly one of source or text")
        return self


class PredictionBlock(TitledBlock):
    type: Literal["prediction"]
    text: NonEmptyString
    reveal: NonEmptyString | None = None


class ControlsBlock(TitledBlock):
    type: Literal["controls"]


class MetricsBlock(TitledBlock):
    type: Literal["metrics"]


class PlotBlock(TitledBlock):
    type: Literal["plot"]
    plot: ResultKey


class PlotGridBlock(TitledBlock):
    type: Literal["plot_grid"]
    plots: list[ResultKey] = Field(min_length=1)

    @field_validator("plots")
    @classmethod
    def validate_unique_plots(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("plot_grid plot references must be unique")
        return value


class TableBlock(TitledBlock):
    type: Literal["table"]
    table: ResultKey


class CalloutBlock(TitledBlock):
    type: Literal["callout"]
    source: ResultKey | None = None
    text: NonEmptyString | None = None
    tone: Literal["info", "success", "warning", "danger"] = "info"

    @model_validator(mode="after")
    def validate_content(self) -> CalloutBlock:
        if (self.source is None) == (self.text is None):
            raise ValueError("callout block requires exactly one of source or text")
        return self


class ParameterMapProps(StrictModel):
    x_control: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    y_control: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    x_label: NonEmptyString
    y_label: NonEmptyString


class WidgetBlock(TitledBlock):
    type: Literal["widget"]
    widget: Literal["parameter-map"]
    props: ParameterMapProps


class DividerBlock(StrictModel):
    type: Literal["divider"]


LessonBlock = Annotated[
    MarkdownBlock
    | PredictionBlock
    | ControlsBlock
    | MetricsBlock
    | PlotBlock
    | PlotGridBlock
    | TableBlock
    | CalloutBlock
    | WidgetBlock
    | DividerBlock,
    Field(discriminator="type"),
]


class ModuleManifest(StrictModel):
    schema_version: SchemaVersion
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    number: int | None = None
    title: NonEmptyString
    summary: str = ""
    guiding_question: str = ""
    status: Literal["draft", "implemented", "static"] = "draft"
    runtime: RuntimeSpec = Field(default_factory=StaticRuntime)
    controls: list[ControlSpec] = Field(default_factory=list)
    blocks: list[LessonBlock] = Field(default_factory=list)
    tags: list[NonEmptyString] = Field(default_factory=list)

    _validate_schema_version = field_validator("schema_version", mode="before")(
        _exact_schema_version
    )

    @model_validator(mode="after")
    def validate_identity(self) -> ModuleManifest:
        ids = [control.id for control in self.controls]
        if len(ids) != len(set(ids)):
            raise ValueError("module control ids must be unique")
        known = set(ids)
        controls = {control.id: control for control in self.controls}
        for control in self.controls:
            if control.visible_when:
                unknown = set(control.visible_when) - known
                if unknown:
                    raise ValueError(f"visible_when references unknown controls: {sorted(unknown)}")
                if control.id in control.visible_when:
                    raise ValueError("visible_when cannot reference its own control")
                for target, expected in control.visible_when.items():
                    referenced = controls[target]
                    if referenced.type == "toggle" and type(expected) is not bool:
                        raise ValueError(f"visible_when value for {target!r} must be boolean")
                    if referenced.type in {"slider", "number"}:
                        if isinstance(expected, bool) or not isinstance(expected, (int, float)):
                            raise ValueError(f"visible_when value for {target!r} must be numeric")
                        if not referenced.minimum <= float(expected) <= referenced.maximum:
                            raise ValueError(
                                f"visible_when value for {target!r} is outside its range"
                            )
                    if referenced.type in {"select", "segmented"} and not any(
                        type(expected) is type(option.value) and expected == option.value
                        for option in referenced.options
                    ):
                        raise ValueError(f"visible_when value for {target!r} must match an option")
        for block in self.blocks:
            if block.type == "widget":
                numeric = {
                    control.id for control in self.controls if control.type in {"slider", "number"}
                }
                for axis in ("x_control", "y_control"):
                    target = getattr(block.props, axis)
                    if target not in numeric:
                        raise ValueError(f"parameter-map {axis} must reference a numeric control")
                if block.props.x_control == block.props.y_control:
                    raise ValueError("parameter-map axes must reference distinct controls")
        if self.runtime.kind == "static" and self.controls:
            raise ValueError("static runtime modules cannot declare live controls")
        if self.runtime.kind == "static" and self.status == "implemented":
            raise ValueError("static runtime modules must use status static or draft")
        return self


class ContentRevision(StrictModel):
    schema_version: SchemaVersion = SCHEMA_VERSION
    content_digest: Digest
    source_git_commit: GitCommit | None


class PlatformRevision(StrictModel):
    platform_version: NonEmptyString
    platform_git_commit: GitCommit | None
    runtime_content_digest: Digest
    runtime_kind: Literal["python-in-process", "static"]


class ModuleSummary(StrictModel):
    id: str
    number: int | None
    title: str
    summary: str
    status: str
    interactive: bool
    revision: ContentRevision


class CourseSummary(StrictModel):
    id: str
    title: str
    description: str
    order: int
    tags: list[str]
    modules: list[ModuleSummary]
    revision: ContentRevision


class ModuleDocument(StrictModel):
    course: CourseSummary
    module: ModuleManifest
    markdown_sources: dict[str, str] = Field(default_factory=dict)
    default_parameters: dict[str, Any] = Field(default_factory=dict)
    module_revision: ContentRevision
    platform_revision: PlatformRevision


class RunRequest(StrictModel):
    parameters: dict[str, Any] = Field(default_factory=dict)
    expected_content_digest: Digest


class Metric(StrictModel):
    id: ResultKey
    label: NonEmptyString
    value: Scalar
    unit: NonEmptyString | None = None
    detail: NonEmptyString | None = None
    emphasis: Literal["normal", "primary", "warning", "danger"] = "normal"


class PlotSpec(StrictModel):
    data: list[dict[str, Any]] = Field(min_length=1)
    layout: dict[str, Any]
    config: dict[str, Any] = Field(default_factory=dict)
    frames: list[dict[str, Any]] = Field(default_factory=list)

    @field_validator("data")
    @classmethod
    def validate_trace_types(cls, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for index, trace in enumerate(value):
            if not isinstance(trace.get("type"), str) or not trace["type"]:
                raise ValueError(f"plot trace {index} requires a non-empty type")
        return value

    @field_validator("layout")
    @classmethod
    def validate_layout_label(cls, value: dict[str, Any]) -> dict[str, Any]:
        def has_text(candidate: Any) -> bool:
            if isinstance(candidate, str):
                return bool(candidate.strip())
            return (
                isinstance(candidate, dict)
                and isinstance(candidate.get("text"), str)
                and bool(candidate["text"].strip())
            )

        candidates: list[Any] = [value.get("title")]
        for axis in ("xaxis", "yaxis"):
            section = value.get(axis)
            if isinstance(section, dict):
                candidates.append(section.get("title"))
        for container, axes in (
            ("scene", ("xaxis", "yaxis", "zaxis")),
            ("polar", ("angularaxis", "radialaxis")),
            ("ternary", ("aaxis", "baxis", "caxis")),
        ):
            section = value.get(container)
            if not isinstance(section, dict):
                continue
            for axis in axes:
                axis_value = section.get(axis)
                if isinstance(axis_value, dict):
                    candidates.append(axis_value.get("title"))
        if not any(has_text(candidate) for candidate in candidates):
            raise ValueError("plot layout requires a non-empty title or axis label")
        return value


class TableSpec(StrictModel):
    columns: list[NonEmptyString] = Field(min_length=1)
    rows: list[dict[str, Any]]

    @model_validator(mode="after")
    def validate_rows(self) -> TableSpec:
        if len(self.columns) != len(set(self.columns)):
            raise ValueError("table columns must be unique")
        expected = set(self.columns)
        for index, row in enumerate(self.rows):
            actual = set(row)
            if actual != expected:
                raise ValueError(
                    f"table row {index} columns must exactly match declaration; "
                    f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
                )
        return self


class RunResult(StrictModel):
    parameters: dict[str, Any]
    metrics: list[Metric] = Field(default_factory=list)
    plots: dict[ResultKey, PlotSpec] = Field(default_factory=dict)
    tables: dict[ResultKey, TableSpec] = Field(default_factory=dict)
    explanations: dict[ResultKey, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    course_revision: ContentRevision
    module_revision: ContentRevision
    platform_revision: PlatformRevision

    @field_validator("metrics")
    @classmethod
    def validate_metric_ids(cls, value: list[Metric]) -> list[Metric]:
        ids = [metric.id for metric in value]
        if len(ids) != len(set(ids)):
            raise ValueError("metric ids must be unique")
        return value
