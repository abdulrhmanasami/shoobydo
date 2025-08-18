'use client'
import React from 'react';

type Row = { category: string; description: string; supplier: string; estCost: string };

const rows: Row[] = [
  { category: 'Smart Water Bottle', description: 'Temp control, eco materials', supplier: 'OEM partner (EU/Asia)', estCost: '€12–€18' },
  { category: 'DIY Craft Kits', description: 'Sustainable hobby bundles', supplier: 'EU artisan network', estCost: '€6–€10' },
  { category: 'Eco Home Decor', description: 'Minimalist, sustainable materials', supplier: 'Benelux supplier', estCost: '€8–€15' },
  { category: 'Bio Beauty Set', description: 'Organic skincare essentials', supplier: 'FR lab/private label', estCost: '€9–€14' },
  { category: 'Fitness Accessories', description: 'Resistance bands, yoga mats', supplier: 'IT manufacturer', estCost: '€7–€12' },
];

export default function ProductsPage(){
  return (
    <main className="main-content">
      <h1 className="page-title">Proposed Products</h1>
      <table className="data-table">
        <thead>
          <tr>
            <th>Category</th>
            <th>Short Description</th>
            <th>Suggested Supplier</th>
            <th>Estimated Cost</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, idx) => (
            <tr key={idx}>
              <td>{r.category}</td>
              <td>{r.description}</td>
              <td>{r.supplier}</td>
              <td>{r.estCost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
