import { useMemo, useRef } from "react";
import { Move, Puzzle } from "lucide-react";
import type { ControlSpec, LessonBlock } from "../types";
import { formatValue } from "../lib/format";

interface Props {
  block: LessonBlock;
  controls: ControlSpec[];
  parameters: Record<string, unknown>;
  onParameter: (id: string, value: unknown) => void;
}

interface AxisBinding {
  control: ControlSpec;
  value: number;
  minimum: number;
  maximum: number;
}

function binding(id: unknown, controls: ControlSpec[], parameters: Record<string, unknown>): AxisBinding | null {
  if (typeof id !== "string") return null;
  const control = controls.find((item) => item.id === id);
  if (!control || !["slider", "number"].includes(control.type) || control.minimum == null || control.maximum == null) return null;
  const value = Number(parameters[id] ?? control.default);
  return { control, value, minimum: control.minimum, maximum: control.maximum };
}

function quantize(value: number, axis: AxisBinding): number {
  const clipped = Math.min(axis.maximum, Math.max(axis.minimum, value));
  if (!axis.control.step) return clipped;
  const steps = Math.round((clipped - axis.minimum) / axis.control.step);
  return Number((axis.minimum + steps * axis.control.step).toPrecision(12));
}

function ParameterMap({ block, controls, parameters, onParameter }: Props) {
  const svg = useRef<SVGSVGElement>(null);
  const x = useMemo(() => binding(block.props.x_control, controls, parameters), [block.props.x_control, controls, parameters]);
  const y = useMemo(() => binding(block.props.y_control, controls, parameters), [block.props.y_control, controls, parameters]);
  if (!x || !y) return <Unsupported name="parameter-map requires two numeric controls" />;
  const left = 60, right = 20, top = 24, bottom = 49, width = 680, height = 300;
  const plotWidth = width - left - right, plotHeight = height - top - bottom;
  const px = left + ((x.value - x.minimum) / (x.maximum - x.minimum)) * plotWidth;
  const py = top + (1 - (y.value - y.minimum) / (y.maximum - y.minimum)) * plotHeight;

  const update = (clientX: number, clientY: number) => {
    const rect = svg.current?.getBoundingClientRect();
    if (!rect) return;
    const localX = ((clientX - rect.left) / rect.width) * width;
    const localY = ((clientY - rect.top) / rect.height) * height;
    const xValue = x.minimum + ((localX - left) / plotWidth) * (x.maximum - x.minimum);
    const yValue = y.minimum + (1 - (localY - top) / plotHeight) * (y.maximum - y.minimum);
    onParameter(x.control.id, quantize(xValue, x));
    onParameter(y.control.id, quantize(yValue, y));
  };

  return (
    <section className="widget-panel">
      <header className="panel-heading">
        <div><span className="eyebrow"><Move size={13} /> direct manipulation</span><h2>{block.title ?? "Parameter map"}</h2></div>
        <span className="plot-hint">drag the probe</span>
      </header>
      <svg
        ref={svg}
        viewBox={`0 0 ${width} ${height}`}
        className="parameter-map"
        role="img"
        aria-label={`${x.control.label} ${formatValue(x.value)}, ${y.control.label} ${formatValue(y.value)}`}
        onPointerDown={(event) => {
          event.currentTarget.setPointerCapture(event.pointerId);
          update(event.clientX, event.clientY);
        }}
        onPointerMove={(event) => {
          if (event.currentTarget.hasPointerCapture(event.pointerId)) update(event.clientX, event.clientY);
        }}
      >
        <rect x={left} y={top} width={plotWidth} height={plotHeight} rx="10" className="map-background" />
        {[0, .25, .5, .75, 1].map((fraction) => (
          <g key={`x-${fraction}`}>
            <line x1={left + fraction * plotWidth} x2={left + fraction * plotWidth} y1={top} y2={top + plotHeight} className="map-grid" />
            <text x={left + fraction * plotWidth} y={top + plotHeight + 19} className="map-tick" textAnchor="middle">{formatValue(x.minimum + fraction * (x.maximum - x.minimum))}</text>
          </g>
        ))}
        {[0, .25, .5, .75, 1].map((fraction) => (
          <g key={`y-${fraction}`}>
            <line x1={left} x2={left + plotWidth} y1={top + fraction * plotHeight} y2={top + fraction * plotHeight} className="map-grid" />
            <text x={left - 9} y={top + fraction * plotHeight + 4} className="map-tick" textAnchor="end">{formatValue(y.maximum - fraction * (y.maximum - y.minimum))}</text>
          </g>
        ))}
        <line x1={px} x2={px} y1={top} y2={top + plotHeight} className="map-crosshair" />
        <line x1={left} x2={left + plotWidth} y1={py} y2={py} className="map-crosshair" />
        <circle cx={px} cy={py} r="11" className="map-probe-halo" />
        <circle cx={px} cy={py} r="6" className="map-probe" />
        <text x={left + plotWidth / 2} y={height - 8} className="map-axis" textAnchor="middle">{String(block.props.x_label ?? `${x.control.label}${x.control.unit ? ` (${x.control.unit})` : ""}`)}</text>
        <text transform={`translate(15 ${top + plotHeight / 2}) rotate(-90)`} className="map-axis" textAnchor="middle">{String(block.props.y_label ?? `${y.control.label}${y.control.unit ? ` (${y.control.unit})` : ""}`)}</text>
      </svg>
      <div className="widget-values"><span>{x.control.label}: <strong>{formatValue(x.value)} {x.control.unit}</strong></span><span>{y.control.label}: <strong>{formatValue(y.value)} {y.control.unit}</strong></span></div>
    </section>
  );
}

function Unsupported({ name }: { name: string }) {
  return <section className="widget-panel unsupported-widget"><Puzzle size={20} /><span>Unsupported widget: {name}</span></section>;
}

export function WidgetRenderer(props: Props) {
  if (props.block.widget === "parameter-map") return <ParameterMap {...props} />;
  return <Unsupported name={props.block.widget ?? "unspecified"} />;
}
