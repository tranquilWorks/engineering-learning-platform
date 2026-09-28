import { useEffect, useId, useRef, useState } from "react";
import { AlertTriangle, Box, RotateCcw } from "lucide-react";
import type { PlotSpec } from "../types";
import { normalizePlotTitles } from "../lib/plotTitles";
import { markWebGLUnavailable, preparePlotData, supportsWebGL } from "../lib/plotRendering";

interface Props {
  title?: string | null;
  spec?: PlotSpec;
  compact?: boolean;
  name?: string;
}

export function PlotPanel({ title, spec, compact = false, name }: Props) {
  const root = useRef<HTMLDivElement>(null);
  const id = useId();
  const [error, setError] = useState<string | null>(null);
  const plain = (value: unknown): string => {
    if (typeof value === "string") return value.replace(/<[^>]*>/g, "");
    if (value && typeof value === "object" && "text" in value) return plain(value.text);
    return "";
  };
  const plotTitle = [title || plain(spec?.layout.title), name?.replace(/_/g, " ")]
    .filter(Boolean).join(": ") || "Numerical evidence";
  const axis = (name: string) => {
    const value = spec?.layout[name];
    return value && typeof value === "object" && "title" in value ? plain(value.title) : "";
  };
  const range = (value: unknown): string => {
    if (!Array.isArray(value)) return "—";
    const values = value.flat().filter((item): item is number => typeof item === "number" && Number.isFinite(item));
    if (!values.length) return `${value.length} categories`;
    let min = Infinity, max = -Infinity;
    for (const item of values) { min = Math.min(min, item); max = Math.max(max, item); }
    return `${values.length} values; ${min.toPrecision(5)} to ${max.toPrecision(5)}`;
  };

  useEffect(() => {
    if (!root.current || !spec) return;
    let active = true;
    const node = root.current;
    setError(null);
    void import("plotly.js-dist-min")
      .then(async ({ default: Plotly }) => {
        if (!active) return;
        const layout: Record<string, unknown> = {
          autosize: true,
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(0,0,0,0)",
          font: { color: "#bdc7db", family: "Inter, ui-sans-serif, system-ui" },
          colorway: ["#67a9ff", "#b396ff", "#53d1a3", "#ffbd66", "#f47b9a"],
          margin: { l: 62, r: 28, t: 52, b: 58 },
          ...normalizePlotTitles(spec.layout),
        };
        const legend = layout.legend as Record<string, unknown> | undefined;
        if (legend?.orientation === "h" && legend.y === undefined) {
          // Reserve a separate bottom band for automatic horizontal legends;
          // the paper-relative default can collide with the x-axis title.
          layout.legend = { ...legend, yref: "container", y: 0, yanchor: "bottom" };
          const margin = layout.margin as Record<string, number>;
          layout.margin = { ...margin, b: Math.max(margin.b ?? 0, 110) };
        }
        if (Object.entries(layout).some(([key, value]) => /^xaxis\d*$/.test(key)
          && (value as Record<string, unknown>)?.side === "top")) {
          const margin = layout.margin as Record<string, number>;
          layout.margin = { ...margin, t: Math.max(margin.t ?? 0, 96) };
          layout.title = { ...(layout.title as Record<string, unknown>), y: 0.98, yanchor: "top" };
        }
        const data = spec.data.map(normalizePlotTitles);
        const config = {
          responsive: true,
          displaylogo: false,
          scrollZoom: true,
          modeBarButtonsToRemove: ["lasso2d", "select2d"],
          ...spec.config,
        };
        const hasGL = data.some(trace => trace.type === "scattergl");
        let retrySVG = false;
        try {
          await Plotly.react(node, preparePlotData(data, supportsWebGL()), layout, config);
        } catch (reason) {
          if (!active || !hasGL) throw reason;
          retrySVG = true;
        }
        // A browser may create a WebGL context yet lack the setup required by
        // the plot backend. Plotly resolves its promise while drawing a notice.
        if (active && hasGL && (retrySVG || node.querySelector(".no-webgl"))) {
          markWebGLUnavailable();
          Plotly.purge(node);
          await Plotly.react(node, preparePlotData(data, false), layout, config);
        }
      })
      .catch((reason: unknown) => {
        if (active) setError(reason instanceof Error ? reason.message : "Plot rendering failed");
      });
    return () => {
      active = false;
      void import("plotly.js-dist-min").then(({ default: Plotly }) => Plotly.purge(node));
    };
  }, [spec, id]);

  if (!spec) {
    return (
      <section className="plot-panel plot-empty">
        <Box size={18} />
        <span>Plot data has not been produced.</span>
      </section>
    );
  }

  return (
    <section aria-label={plotTitle} className={`plot-panel ${compact ? "plot-panel-compact" : ""}`}>
      {title ? (
        <header className="panel-heading">
          <div>
            <span className="eyebrow">Live visualization</span>
            <h2>{title}</h2>
          </div>
          <span className="plot-hint"><RotateCcw size={13} /> double-click to reset</span>
        </header>
      ) : null}
      {error ? (
        <div className="error-inline"><AlertTriangle size={17} /> {error}</div>
      ) : (
        <div ref={root} role="group" aria-label={`${plotTitle}. Numeric ranges follow the plot.`} className="plot-canvas" />
      )}
      <details className="plot-values">
        <summary>Numeric ranges: {plotTitle}</summary>
        <p>Use the lesson interpretation and metrics to explain these ranges. Ranges summarize samples; they do not describe the full curve.</p>
        <div className="table-scroll" tabIndex={0} role="group" aria-label={`${plotTitle} numeric ranges`}><table>
          <thead><tr><th>Series</th><th>{axis("xaxis") || "x"}</th><th>{axis("yaxis") || "y"}</th><th>z (if present)</th></tr></thead>
          <tbody>{spec.data.map((trace, index) => <tr key={index}><th>{plain(trace.name) || `Series ${index + 1}`}</th><td>{range(trace.x)}</td><td>{range(trace.y)}</td><td>{range(trace.z)}</td></tr>)}</tbody>
        </table></div>
      </details>
    </section>
  );
}
