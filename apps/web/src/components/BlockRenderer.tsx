import type { CalloutBlock, ModuleDocument, RunResult } from "../types";
import { Controls } from "./Controls";
import { DataTable } from "./DataTable";
import { Markdown } from "./Markdown";
import { Metrics } from "./Metrics";
import { PlotPanel } from "./PlotPanel";
import { Prediction } from "./Prediction";
import { WidgetRenderer } from "./WidgetRenderer";

interface Props {
  document: ModuleDocument;
  result: RunResult | null;
  parameters: Record<string, unknown>;
  busy: boolean;
  onParameter: (id: string, value: unknown) => void;
  onReset: () => void;
}

function Callout({ block, result }: { block: CalloutBlock; result: RunResult | null }) {
  const dynamic = block.source ? result?.explanations[block.source] : undefined;
  return (
    <section className={`callout callout-${block.tone}`}>
      {block.title ? <h2>{block.title}</h2> : null}
      <p>{dynamic ?? block.text ?? ""}</p>
    </section>
  );
}

export function BlockRenderer({ document, result, parameters, busy, onParameter, onReset }: Props) {
  return (
    <div className="lesson-blocks">
      <nav className="lesson-jumps" aria-label="Lesson sections">
        {document.module.blocks.map((block, index) => {
          const labels: Record<string, string> = { markdown: "Concept", prediction: "Predict", controls: "Experiment", metrics: "Evidence" };
          const label = labels[block.type];
          if (block.type === "controls") return <span key={index}><a className="lesson-jump-desktop" href="#experiment-settings">Experiment</a><a className="lesson-jump-mobile" href={`#lesson-block-${index}`}>Experiment</a></span>;
          return label && document.module.blocks.findIndex((item) => item.type === block.type) === index ? <a key={index} href={`#lesson-block-${index}`}>{label}</a> : null;
        })}
      </nav>
      {document.module.blocks.map((block, index) => {
        const key = `${document.module.id}-${block.type}-${index}`;
        if (block.type === "markdown") {
          const markdown = block.source ? document.markdown_sources[block.source] : block.text;
          return markdown ? <section key={key} id={`lesson-block-${index}`} className="narrative-panel"><Markdown courseId={document.course.id} moduleId={document.module.id}>{markdown}</Markdown></section> : null;
        }
        if (block.type === "prediction") return <div key={key} id={`lesson-block-${index}`}><Prediction title={block.title} prompt={block.text ?? ""} reveal={block.reveal} /></div>;
        if (block.type === "controls") {
          return (
            <div key={key} id={`lesson-block-${index}`} className="mobile-controls">
              <Controls controls={document.module.controls} parameters={parameters} busy={busy} onChange={onParameter} onReset={onReset} />
            </div>
          );
        }
        if (block.type === "metrics") return <div key={key} id={`lesson-block-${index}`}><Metrics metrics={result?.metrics ?? []} /></div>;
        if (block.type === "plot") return <PlotPanel key={key} title={block.title} name={block.plot} spec={block.plot ? result?.plots[block.plot] : undefined} />;
        if (block.type === "plot_grid") {
          return (
            <section key={key} className="plot-grid-section">
              {block.title ? <div className="section-heading"><span className="eyebrow">Linked views</span><h2>{block.title}</h2></div> : null}
              <div className="plot-grid">
                {block.plots.map((name) => <PlotPanel key={name} name={name} compact spec={result?.plots[name]} />)}
              </div>
            </section>
          );
        }
        if (block.type === "table") return <DataTable key={key} title={block.title} table={block.table ? result?.tables[block.table] : undefined} />;
        if (block.type === "widget") return <WidgetRenderer key={key} block={block} controls={document.module.controls} parameters={parameters} onParameter={onParameter} />;
        if (block.type === "callout") return <Callout key={key} block={block} result={result} />;
        return <hr key={key} className="lesson-divider" />;
      })}
    </div>
  );
}
