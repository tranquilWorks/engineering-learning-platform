/// <reference types="vite/client" />

declare module "plotly.js-dist-min" {
  interface PlotlyRuntime {
    react(
      element: HTMLElement,
      data: Record<string, unknown>[],
      layout?: Record<string, unknown>,
      config?: Record<string, unknown>,
    ): Promise<unknown>;
    purge(element: HTMLElement): void;
  }
  const Plotly: PlotlyRuntime;
  export default Plotly;
}
