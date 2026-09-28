/** Adapt portable legacy title strings to Plotly 3 without changing course data. */
export function normalizePlotTitles(value: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(Object.entries(value).map(([key, item]) => [key,
    key === 'title' && typeof item === 'string' ? { text: item }
      : item && typeof item === 'object' && !Array.isArray(item)
        ? normalizePlotTitles(item as Record<string, unknown>) : item,
  ]));
}
