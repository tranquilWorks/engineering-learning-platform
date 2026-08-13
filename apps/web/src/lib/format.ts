export function formatValue(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "boolean") return value ? "On" : "Off";
  if (typeof value !== "number") return String(value);
  if (!Number.isFinite(value)) return String(value);
  const magnitude = Math.abs(value);
  if ((magnitude > 0 && magnitude < 0.001) || magnitude >= 1e7) return value.toExponential(3);
  if (Number.isInteger(value)) return value.toLocaleString();
  const digits = magnitude >= 100 ? 2 : magnitude >= 1 ? 3 : 5;
  return value.toLocaleString(undefined, { maximumFractionDigits: digits });
}
