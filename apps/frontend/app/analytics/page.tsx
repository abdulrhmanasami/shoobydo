"use client";
import React, { useEffect, useState } from "react";

type Stats = { total:number; files:number; rows:number; sheets:number };
type KPISummary = { files:number; rows:number; sheets:number };
type Costs = { total_cost:number; total_margin:number };

export default function AnalyticsPage(){
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [sup,setSup]=useState<Stats|null>(null);
  const [kpi,setKpi]=useState<KPISummary|null>(null);
  const [cost,setCost]=useState<Costs|null>(null);
  const [err,setErr]=useState<string|null>(null);

  useEffect(()=>{(async()=>{
    try{
      const [s,k,c] = await Promise.all([
        fetch(`${API}/suppliers/stats`).then(r=>r.json()),
        fetch(`${API}/reports/kpis`).then(r=>r.json()),
        fetch(`${API}/reports/costs`).then(r=>r.json()),
      ]);
      setSup(s); setKpi(k); setCost(c);
    }catch(e:any){ setErr(String(e)); }
  })();},[API]);

  const chartData = [
    { name: 'Suppliers', value: sup?.total ?? 0 },
    { name: 'Excel Files', value: kpi?.files ?? 0 },
    { name: 'Rows', value: kpi?.rows ?? 0 },
    { name: 'Total Cost', value: cost?.total_cost ?? 0 },
    { name: 'Total Margin', value: cost?.total_margin ?? 0 },
  ];

  let Chart: React.ReactNode = null;
  try {
    const Recharts = require('recharts');
    const ResponsiveContainer = Recharts.ResponsiveContainer;
    const BarChart = Recharts.BarChart;
    const Bar = Recharts.Bar;
    const XAxis = Recharts.XAxis;
    const YAxis = Recharts.YAxis;
    const Tooltip = Recharts.Tooltip;
    const CartesianGrid = Recharts.CartesianGrid;
    Chart = (
      <div className="mt-4" style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#34d399" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  } catch {}

  return (
    <main className="main space-y-6">
      <h1 className="h1">Analytics</h1>
      {err && <pre className="text-error">{err}</pre>}
      {Chart}
    </main>
  );
}


