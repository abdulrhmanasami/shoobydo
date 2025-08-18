"use client";
import React, { useState } from "react";

export default function UploadPage(){
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent){
    e.preventDefault();
    setMsg(null); setErr(null);
    if(!file){ setErr("Please choose a .xlsx file"); return; }
    const fd = new FormData();
    fd.append('file', file);
    try{
      const res = await fetch(`${API}/suppliers/upload`, { method:'POST', body: fd });
      if(!res.ok){ throw new Error(await res.text()); }
      const j = await res.json();
      setMsg(`Uploaded: ${j.saved}`);
    }catch(e:any){ setErr(String(e)); }
  }

  return (
    <main className="main space-y-6">
      <h1 className="h1">Upload Excel</h1>
      {err && <pre className="text-error">{err}</pre>}
      {msg && <div style={{color:'#059669'}}>{msg}</div>}
      <form onSubmit={onSubmit} className="space-y-6">
        <input type="file" accept=".xlsx" onChange={e=> setFile(e.target.files?.[0] || null)} />
        <button type="submit" className="btn">Upload</button>
      </form>
    </main>
  );
}


