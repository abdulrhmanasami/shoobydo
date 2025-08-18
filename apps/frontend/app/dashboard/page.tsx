'use client'
import React,{useEffect,useState} from 'react';

type Summary = { suppliers:number; kpis:number; notes?:string };
type KPISummary = { files:number; rows:number; sheets:number; notes?:string };

export default function Page(){
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [summary,setSummary]=useState<Summary|null>(null);
  const [kpis,setKpis]=useState<KPISummary|null>(null);
  const [err,setErr]=useState<string|null>(null);

  useEffect(() => {
    async function load(){
      try{
        const [s, k] = await Promise.all([
          fetch(`${API}/reports/summary`).then(r => r.json()),
          fetch(`${API}/reports/kpis`).then(r => r.json()),
        ]);
        setSummary(s); setKpis(k);
      } catch(e:any){ setErr(String(e)); }
    }
    load();
  }, [API]);

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <p className="text-sm opacity-70">API: {API}</p>
      {err && <pre className="text-red-600">{err}</pre>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl shadow">Suppliers: {summary?.suppliers ?? '—'}</div>
        <div className="p-4 rounded-2xl shadow">Excel files: {kpis?.files ?? '—'}</div>
        <div className="p-4 rounded-2xl shadow">Rows (approx): {kpis?.rows ?? '—'}</div>
      </div>
    </main>
  )
}
