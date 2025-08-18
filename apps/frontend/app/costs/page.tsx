"use client";
import React, { useEffect, useState } from "react";

type Costs = { files: number; rows: number; total_cost: number; total_margin: number; notes?: string };

export default function CostsPage() {
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [data, setData] = useState<Costs | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API}/reports/costs`);
        const j = await res.json();
        setData(j);
      } catch (e: any) {
        setErr(String(e));
      }
    }
    load();
  }, [API]);

  const chartData = data
    ? [
        { name: "Total Cost", value: data.total_cost },
        { name: "Total Margin", value: data.total_margin },
      ]
    : [];

  let Chart: React.ReactNode = null;
  try {
    // Lazy require so build doesn't fail if not installed yet
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const Recharts = require("recharts");
    const ResponsiveContainer = Recharts.ResponsiveContainer;
    const BarChart = Recharts.BarChart;
    const Bar = Recharts.Bar;
    const XAxis = Recharts.XAxis;
    const YAxis = Recharts.YAxis;
    const Tooltip = Recharts.Tooltip;
    const CartesianGrid = Recharts.CartesianGrid;
    Chart = (
      <div className="mt-4" style={{ width: "100%", height: 280 }}>
        <ResponsiveContainer>
          <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#60a5fa" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  } catch {}

  return (
    <main className="main space-y-6">
      <h1 className="h1">Costs</h1>
      {err && <pre className="text-error">{err}</pre>}
      {data && (
        <>
          <table className="table">
            <thead>
              <tr>
                <th>Files</th>
                <th>Rows</th>
                <th>Total Cost</th>
                <th>Total Margin</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{data.files}</td>
                <td>{data.rows}</td>
                <td>{data.total_cost}</td>
                <td>{data.total_margin}</td>
                <td>{data.notes || "-"}</td>
              </tr>
            </tbody>
          </table>
          {Chart}
        </>
      )}
    </main>
  );
}


