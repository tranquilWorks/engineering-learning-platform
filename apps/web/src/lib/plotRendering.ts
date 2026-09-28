let webglAvailable: boolean | undefined;

/** Probe once and release the probe context; do not consume a context per plot. */
export function supportsWebGL(): boolean {
  if (webglAvailable !== undefined) return webglAvailable;
  if (typeof document === "undefined") return false;
  const canvas = document.createElement("canvas");
  try {
    const context = canvas.getContext("webgl");
    webglAvailable = context !== null;
    context?.getExtension("WEBGL_lose_context")?.loseContext();
  } catch {
    webglAvailable = false;
  }
  return webglAvailable;
}

/** Context creation alone can succeed while the chart's required setup fails. */
export function markWebGLUnavailable(): void {
  webglAvailable = false;
}

/** Preserve coordinates and trace attributes; only the 2D rendering backend changes. */
export function preparePlotData(
  data: Array<Record<string, unknown>>,
  webglSupported: boolean,
): Array<Record<string, unknown>> {
  return data.map(trace => !webglSupported && trace.type === "scattergl"
    ? { ...trace, type: "scatter" }
    : trace);
}
