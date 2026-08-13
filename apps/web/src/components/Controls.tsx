import { RotateCcw, Sparkles } from "lucide-react";
import type { ControlSpec } from "../types";
import { formatValue } from "../lib/format";

interface Props {
  controls: ControlSpec[];
  parameters: Record<string, unknown>;
  busy: boolean;
  onChange: (id: string, value: unknown) => void;
  onReset: () => void;
}

function isVisible(control: ControlSpec, parameters: Record<string, unknown>): boolean {
  if (!control.visible_when) return true;
  return Object.entries(control.visible_when).every(([key, expected]) => parameters[key] === expected);
}

export function Controls({ controls, parameters, busy, onChange, onReset }: Props) {
  return (
    <section className="control-panel" aria-label="Experiment controls">
      <header className="control-panel-header">
        <div>
          <span className="eyebrow"><Sparkles size={13} /> experiment</span>
          <h2>Controls</h2>
        </div>
        <button className="icon-button" type="button" onClick={onReset} title="Reset parameters">
          <RotateCcw size={16} />
        </button>
      </header>
      <div className="control-list">
        {controls.filter((control) => isVisible(control, parameters)).map((control) => {
          const value = parameters[control.id] ?? control.default;
          if (control.type === "toggle") {
            return (
              <label key={control.id} className="toggle-row">
                <span>
                  <strong>{control.label}</strong>
                  {control.description ? <small>{control.description}</small> : null}
                </span>
                <input
                  type="checkbox"
                  checked={Boolean(value)}
                                    onChange={(event) => onChange(control.id, event.target.checked)}
                />
              </label>
            );
          }
          if (control.type === "select") {
            return (
              <label key={control.id} className="control-field">
                <span className="control-label">{control.label}</span>
                <select
                  value={String(value)}
                                    onChange={(event) => {
                    const selected = control.options.find((option) => String(option.value) === event.target.value);
                    onChange(control.id, selected?.value ?? event.target.value);
                  }}
                >
                  {control.options.map((option) => <option key={String(option.value)} value={String(option.value)}>{option.label}</option>)}
                </select>
                {control.description ? <small>{control.description}</small> : null}
              </label>
            );
          }
          if (control.type === "segmented") {
            return (
              <fieldset key={control.id} className="control-field segmented-field">
                <legend className="control-label">{control.label}</legend>
                <div className="segmented">
                  {control.options.map((option) => (
                    <button
                      key={String(option.value)}
                      type="button"
                      className={String(value) === String(option.value) ? "active" : ""}
                                            onClick={() => onChange(control.id, option.value)}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </fieldset>
            );
          }
          if (control.type === "button") {
            return (
              <button
                key={control.id}
                type="button"
                className="action-control"
                                onClick={() => onChange(control.id, Date.now())}
              >
                {control.label}
              </button>
            );
          }
          const numeric = typeof value === "number" ? value : Number(value);
          return (
            <label key={control.id} className="control-field">
              <span className="control-label control-label-split">
                <span>{control.label}</span>
                <output>{formatValue(numeric)}{control.unit ? ` ${control.unit}` : ""}</output>
              </span>
              {control.type === "slider" ? (
                <input
                  type="range"
                  min={control.minimum ?? undefined}
                  max={control.maximum ?? undefined}
                  step={control.step ?? "any"}
                  value={numeric}
                                    onChange={(event) => onChange(control.id, Number(event.target.value))}
                />
              ) : (
                <div className="number-input-wrap">
                  <input
                    type="number"
                    min={control.minimum ?? undefined}
                    max={control.maximum ?? undefined}
                    step={control.step ?? "any"}
                    value={numeric}
                                        onChange={(event) => onChange(control.id, Number(event.target.value))}
                  />
                  {control.unit ? <span>{control.unit}</span> : null}
                </div>
              )}
              {control.description ? <small>{control.description}</small> : null}
            </label>
          );
        })}
      </div>
      <div className="compute-status" aria-live="polite">
        <span className={busy ? "status-dot running" : "status-dot"} />
        {busy ? "Recomputing…" : "Experiment synchronized"}
      </div>
    </section>
  );
}
