from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CourseManifest(StrictModel):
    schema_version: int = 1
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    title: str
    description: str = ""
    order: int = 0
    modules_path: str = "modules"
    tags: list[str] = Field(default_factory=list)


class ControlOption(StrictModel):
    label: str
    value: str | int | float | bool


class ControlSpec(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    type: Literal["slider", "number", "toggle", "select", "button", "segmented"]
    label: str
    default: Any = None
    description: str | None = None
    unit: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    step: float | None = None
    options: list[ControlOption] = Field(default_factory=list)
    visible_when: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_control(self) -> "ControlSpec":
        if self.type in {"slider", "number"}:
            if self.minimum is None or self.maximum is None:
                raise ValueError(f"{self.type} control requires minimum and maximum")
            if self.minimum >= self.maximum:
                raise ValueError(f"{self.type} control minimum must be below maximum")
            if self.step is not None and self.step <= 0:
                raise ValueError(f"{self.type} control step must be positive")
            if isinstance(self.default, bool) or not isinstance(self.default, (int, float)):
                raise ValueError(f"{self.type} control default must be numeric")
            if not self.minimum <= float(self.default) <= self.maximum:
                raise ValueError(f"{self.type} control default must be inside its range")
        if self.type == "toggle" and not isinstance(self.default, bool):
            raise ValueError("toggle control default must be boolean")
        if self.type in {"select", "segmented"}:
            if not self.options:
                raise ValueError(f"{self.type} control requires options")
            if not any(type(self.default) is type(option.value) and self.default == option.value for option in self.options):
                raise ValueError(f"{self.type} control default must match one option")
        return self


class RuntimeSpec(StrictModel):
    kind: Literal["python", "static"] = "static"
    entrypoint: str | None = None
    trust: Literal["local-trusted"] = "local-trusted"
    timeout_seconds: float | None = None

    @model_validator(mode="after")
    def validate_entrypoint(self) -> "RuntimeSpec":
        if self.kind == "python" and not self.entrypoint:
            raise ValueError("python runtime requires an entrypoint")
        return self


class LessonBlock(StrictModel):
    type: Literal[
        "markdown",
        "prediction",
        "controls",
        "metrics",
        "plot",
        "plot_grid",
        "table",
        "callout",
        "widget",
        "divider",
    ]
    title: str | None = None
    source: str | None = None
    text: str | None = None
    plot: str | None = None
    plots: list[str] = Field(default_factory=list)
    table: str | None = None
    tone: Literal["info", "success", "warning", "danger"] = "info"
    reveal: str | None = None
    widget: str | None = None
    props: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_block(self) -> "LessonBlock":
        if self.type == "markdown" and not (self.source or self.text):
            raise ValueError("markdown block requires source or text")
        if self.type == "prediction" and not self.text:
            raise ValueError("prediction block requires text")
        if self.type == "plot" and not self.plot:
            raise ValueError("plot block requires plot")
        if self.type == "plot_grid" and not self.plots:
            raise ValueError("plot_grid block requires plots")
        if self.type == "table" and not self.table:
            raise ValueError("table block requires table")
        if self.type == "callout" and not (self.source or self.text):
            raise ValueError("callout block requires source or text")
        if self.type == "widget" and not self.widget:
            raise ValueError("widget block requires widget")
        return self


class ModuleManifest(StrictModel):
    schema_version: int = 1
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    number: int | None = None
    title: str
    summary: str = ""
    guiding_question: str = ""
    status: Literal["draft", "implemented", "static"] = "draft"
    runtime: RuntimeSpec = Field(default_factory=RuntimeSpec)
    controls: list[ControlSpec] = Field(default_factory=list)
    blocks: list[LessonBlock] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_identity(self) -> "ModuleManifest":
        ids = [control.id for control in self.controls]
        if len(ids) != len(set(ids)):
            raise ValueError("module control ids must be unique")
        known = set(ids)
        for control in self.controls:
            if control.visible_when:
                unknown = set(control.visible_when) - known
                if unknown:
                    raise ValueError(f"visible_when references unknown controls: {sorted(unknown)}")
        if self.runtime.kind == "static" and self.controls:
            raise ValueError("static runtime modules cannot declare live controls")
        if self.runtime.kind == "static" and self.status == "implemented":
            # Static modules should declare static status so catalog metadata is honest.
            raise ValueError("static runtime modules must use status static or draft")
        return self


class ModuleSummary(StrictModel):
    id: str
    number: int | None
    title: str
    summary: str
    status: str
    interactive: bool


class CourseSummary(StrictModel):
    id: str
    title: str
    description: str
    order: int
    tags: list[str]
    modules: list[ModuleSummary]


class ModuleDocument(StrictModel):
    course: CourseSummary
    module: ModuleManifest
    markdown_sources: dict[str, str] = Field(default_factory=dict)
    default_parameters: dict[str, Any] = Field(default_factory=dict)


class RunRequest(StrictModel):
    parameters: dict[str, Any] = Field(default_factory=dict)


class Metric(StrictModel):
    id: str
    label: str
    value: int | float | str | bool | None
    unit: str | None = None
    detail: str | None = None
    emphasis: Literal["normal", "primary", "warning", "danger"] = "normal"


class PlotSpec(BaseModel):
    model_config = ConfigDict(extra="allow")
    data: list[dict[str, Any]] = Field(default_factory=list)
    layout: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)
    frames: list[dict[str, Any]] = Field(default_factory=list)


class TableSpec(StrictModel):
    columns: list[str]
    rows: list[dict[str, Any]]


class RunResult(StrictModel):
    parameters: dict[str, Any]
    metrics: list[Metric] = Field(default_factory=list)
    plots: dict[str, PlotSpec] = Field(default_factory=dict)
    tables: dict[str, TableSpec] = Field(default_factory=dict)
    explanations: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
