import { useEffect, useId, useRef, useState } from "react";
import { AlertTriangle, Box, RotateCcw } from "lucide-react";
import type { PlotSpec } from "../types";

interface Props {
  title?: string | null;
  spec?: PlotSpec;
  compact?: boolean;
}

export function PlotPanel({ title, spec, compact = false }: Props) {
  const root = useRef<HTMLDivElement>(null);
  const id = useId();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!root.current || !spec) return;
    let active = true;
    const node = root.current;
    setError(null);
    void import("plotly.js-dist-min")
      .then(({ default: Plotly }) => {
        if (!active) return;
        const layout: Record<string, unknown> = {
          autosize: true,
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(0,0,0,0)",
          font: { color: "#bdc7db", family: "Inter, ui-sans-serif, system-ui" },
          colorway: ["#67a9ff", "#b396ff", "#53d1a3", "#ffbd66", "#f47b9a"],
          margin: { l: 62, r: 28, t: 52, b: 58 },
          ...spec.layout,
        };
        return Plotly.react(node, spec.data, layout, {
          responsive: true,
          displaylogo: false,
          scrollZoom: true,
          modeBarButtonsToRemove: ["lasso2d", "select2d"],
          ...spec.config,
        });
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
    <section className={`plot-panel ${compact ? "plot-panel-compact" : ""}`}>
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
        <div ref={root} aria-label={title ?? "Interactive numerical plot"} className="plot-canvas" />
      )}
    </section>
  );
}
