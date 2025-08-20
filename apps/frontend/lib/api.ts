export const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8805";
export function authHeader(): Record<string,string> {
  if (typeof window === "undefined") return {};
  const t = window.localStorage.getItem("token");
  return t ? { Authorization: `Bearer ${t}` } : {};
}
export async function apiFetch(path: string, init: RequestInit = {}) {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: { "Content-Type":"application/json", ...(init.headers||{}), ...authHeader() },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
