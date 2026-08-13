import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { useMemo } from "react";
import type { TableSpec } from "../types";
import { formatValue } from "../lib/format";

export function DataTable({ title, table }: { title?: string | null; table?: TableSpec }) {
  const columns = useMemo(
    () => (table?.columns ?? []).map((key) => ({ accessorKey: key, header: key })),
    [table?.columns],
  );
  const instance = useReactTable({ data: table?.rows ?? [], columns, getCoreRowModel: getCoreRowModel() });
  if (!table) return <div className="empty-panel">Table data has not been produced.</div>;
  return (
    <section className="table-panel">
      {title ? <div className="panel-heading"><div><span className="eyebrow">Data frame</span><h2>{title}</h2></div></div> : null}
      <div className="table-scroll">
        <table>
          <thead>
            {instance.getHeaderGroups().map((group) => (
              <tr key={group.id}>{group.headers.map((header) => <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>)}</tr>
            ))}
          </thead>
          <tbody>
            {instance.getRowModel().rows.map((row) => (
              <tr key={row.id}>{row.getVisibleCells().map((cell) => <td key={cell.id}>{formatValue(cell.getValue())}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
