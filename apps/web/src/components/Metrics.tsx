import type { Metric } from "../types";
import { formatValue } from "../lib/format";

export function Metrics({ metrics }: { metrics: Metric[] }) {
  if (!metrics.length) return null;
  return (
    <section className="metrics-grid" aria-label="Live metrics">
      {metrics.map((metric) => (
        <article key={metric.id} className={`metric metric-${metric.emphasis}`}>
          <span>{metric.label}</span>
          <strong>{formatValue(metric.value)}{metric.unit ? <small> {metric.unit}</small> : null}</strong>
          {metric.detail ? <p>{metric.detail}</p> : null}
        </article>
      ))}
    </section>
  );
}
