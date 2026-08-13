export type Scalar = string | number | boolean | null;

export interface ControlOption {
  label: string;
  value: Exclude<Scalar, null>;
}

export interface ControlSpec {
  id: string;
  type: "slider" | "number" | "toggle" | "select" | "button" | "segmented";
  label: string;
  default: unknown;
  description?: string | null;
  unit?: string | null;
  minimum?: number | null;
  maximum?: number | null;
  step?: number | null;
  options: ControlOption[];
  visible_when?: Record<string, unknown> | null;
}

export interface RuntimeSpec {
  kind: "python" | "static";
  entrypoint?: string | null;
  trust: "local-trusted";
  timeout_seconds?: number | null;
}

export type LessonBlockType =
  | "markdown"
  | "prediction"
  | "controls"
  | "metrics"
  | "plot"
  | "plot_grid"
  | "table"
  | "callout"
  | "widget"
  | "divider";

export interface LessonBlock {
  type: LessonBlockType;
  title?: string | null;
  source?: string | null;
  text?: string | null;
  plot?: string | null;
  plots: string[];
  table?: string | null;
  tone: "info" | "success" | "warning" | "danger";
  reveal?: string | null;
  widget?: string | null;
  props: Record<string, unknown>;
}

export interface ModuleManifest {
  schema_version: number;
  id: string;
  number?: number | null;
  title: string;
  summary: string;
  guiding_question: string;
  status: "draft" | "implemented" | "static";
  runtime: RuntimeSpec;
  controls: ControlSpec[];
  blocks: LessonBlock[];
  tags: string[];
}

export interface ModuleSummary {
  id: string;
  number?: number | null;
  title: string;
  summary: string;
  status: string;
  interactive: boolean;
}

export interface CourseSummary {
  id: string;
  title: string;
  description: string;
  order: number;
  tags: string[];
  modules: ModuleSummary[];
}

export interface ModuleDocument {
  course: CourseSummary;
  module: ModuleManifest;
  markdown_sources: Record<string, string>;
  default_parameters: Record<string, unknown>;
}

export interface Metric {
  id: string;
  label: string;
  value: Scalar;
  unit?: string | null;
  detail?: string | null;
  emphasis: "normal" | "primary" | "warning" | "danger";
}

export interface PlotSpec {
  data: Record<string, unknown>[];
  layout: Record<string, unknown>;
  config: Record<string, unknown>;
  frames?: Record<string, unknown>[];
}

export interface TableSpec {
  columns: string[];
  rows: Record<string, unknown>[];
}

export interface RunResult {
  parameters: Record<string, unknown>;
  metrics: Metric[];
  plots: Record<string, PlotSpec>;
  tables: Record<string, TableSpec>;
  explanations: Record<string, string>;
  warnings: string[];
  diagnostics: Record<string, unknown>;
}
