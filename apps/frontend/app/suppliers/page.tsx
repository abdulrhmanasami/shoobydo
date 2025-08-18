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
    <main className="main space-y-6">
      <h1 className="h1">Suppliers</h1>
      {err && <pre className="text-error">{err}</pre>}
      <button onClick={reindex} className="btn">Reindex Suppliers</button>
      {stats && (
        <div className="mt-4">
          <p>Total suppliers: {stats.total}</p>
          <p>Total rows: {stats.rows}</p>
          <p>Total sheets: {stats.sheets}</p>
        </div>
      )}
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Rows</th>
            <th>Sheets</th>
          </tr>
        </thead>
        <tbody>
          {suppliers.map(s => (
            <tr key={s.id}>
              <td>{s.id}</td>
              <td>{s.name}</td>
              <td>{s.rows}</td>
              <td>{s.sheets}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
