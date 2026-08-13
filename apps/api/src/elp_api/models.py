from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CourseManifest(StrictModel):
    schema_version: int = 1
    id: str
    title: str
    description: str = ""
    order: int = 0
    modules_path: str = "modules"
    tags: list[str] = Field(default_factory=list)


class ControlOption(StrictModel):
    label: str
    value: str | int | float | bool


class ControlSpec(StrictModel):
    id: str
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
        if self.type in {"select", "segmented"} and not self.options:
            raise ValueError(f"{self.type} control requires options")
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


class ModuleManifest(StrictModel):
    schema_version: int = 1
    id: str
    number: int | None = None
    title: str
    summary: str = ""
    guiding_question: str = ""
    status: Literal["draft", "implemented", "static"] = "draft"
    runtime: RuntimeSpec = Field(default_factory=RuntimeSpec)
    controls: list[ControlSpec] = Field(default_factory=list)
    blocks: list[LessonBlock] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


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
