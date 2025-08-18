'use client'
import React from 'react';

export default function BrandPage(){
  return (
    <main className="main-content">
      <h1 className="page-title">Brand Identity</h1>
      <section className="brand-section">
        <h2>Logo</h2>
        <img src="/assets/logo.png" alt="Brand Logo" style={{height: 64}} />
        <p>Use the primary logo on light backgrounds. Minimum nav height: 24px.</p>
      </section>

      <section className="brand-section">
        <h2>Colors</h2>
        <div className="color-row">
          <div className="swatch" style={{background:'#1F3A5F'}} />
          <code>#1F3A5F</code>
        </div>
        <div className="color-row">
          <div className="swatch" style={{background:'#4A7A8C'}} />
          <code>#4A7A8C</code>
        </div>
        <div className="color-row">
          <div className="swatch" style={{background:'#E0A458'}} />
          <code>#E0A458</code>
        </div>
      </section>

      <section className="brand-section">
        <h2>Typography</h2>
        <p className="brand-heading">Heading Example – Inter/Segoe UI</p>
        <p>Body Example – Inter/Segoe UI regular text for paragraphs.</p>
      </section>
    </main>
  );
}
