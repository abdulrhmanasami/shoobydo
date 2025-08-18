"use client";
import React,{useEffect,useState} from 'react';

type Supplier = { id:number; name:string; file_path:string; rows:number; sheets:number };
type StatResp = { total:number; files:number; rows:number; sheets:number; notes?:string };

export default function SuppliersPage(){
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [suppliers,setSuppliers] = useState<Supplier[]>([]);
  const [stats,setStats] = useState<StatResp|null>(null);
  const [err,setErr] = useState<string|null>(null);

  async function load(){
    try{
      const [list,stat] = await Promise.all([
        fetch(`${API}/suppliers`).then(r=>r.json()),
        fetch(`${API}/suppliers/stats`).then(r=>r.json()),
      ]);
      setSuppliers(list); setStats(stat);
    } catch(e:any){ setErr(String(e)); }
  }

  useEffect(() => { load(); }, []);

  async function reindex(){
    try{
      await fetch(`${API}/suppliers/reindex`,{ method:'POST' });
      await load();
    } catch(e:any){ setErr(String(e)); }
  }

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-semibold">Suppliers</h1>
      {err && <pre className="text-red-600">{err}</pre>}
      <button onClick={reindex} className="px-4 py-2 rounded-md bg-blue-600 text-white">Reindex Suppliers</button>
      {stats && (
        <div className="mt-4">
          <p>Total suppliers: {stats.total}</p>
          <p>Total rows: {stats.rows}</p>
          <p>Total sheets: {stats.sheets}</p>
        </div>
      )}
      <table className="min-w-full border mt-4">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2 border">ID</th>
            <th className="px-4 py-2 border">Name</th>
            <th className="px-4 py-2 border">Rows</th>
            <th className="px-4 py-2 border">Sheets</th>
          </tr>
        </thead>
        <tbody>
          {suppliers.map(s => (
            <tr key={s.id} className="text-sm">
              <td className="px-4 py-2 border">{s.id}</td>
              <td className="px-4 py-2 border">{s.name}</td>
              <td className="px-4 py-2 border">{s.rows}</td>
              <td className="px-4 py-2 border">{s.sheets}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
