export const metadata = {
  title: 'Shoobydo',
  description: 'EuroDropship UI',
};

import './globals.css';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <div className="container header-inner">
            <div className="brand">
              <Link href="/">
                <img src="/logo.png" alt="Logo" className="brand-logo" />
              </Link>
              <span className="brand-name">EuroDropship</span>
            </div>
            <nav className="main-nav">
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/suppliers">Suppliers</Link>
              <Link href="/products">Products</Link>
              <Link href="/costs">Costs</Link>
              <Link href="/analytics">Analytics</Link>
              <Link href="/brand">Brand</Link>
              <Link href="/upload">Upload</Link>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}


