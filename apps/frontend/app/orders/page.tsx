"use client";
import React, { useEffect, useState } from "react";

type Order = {
  id: number;
  customer_id: number;
  status: string;
  currency: string;
  total: number;
  notes?: string;
  created_at: string;
  updated_at: string;
};

type Customer = {
  id: number;
  name: string;
  email: string;
};

export default function OrdersPage() {
  const API = process.env.NEXT_PUBLIC_API_BASE!;
  const [orders, setOrders] = useState<Order[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [ordersRes, customersRes] = await Promise.all([
          fetch(`${API}/orders`),
          fetch(`${API}/customers`)
        ]);
        
        if (!ordersRes.ok) throw new Error(`Orders: ${ordersRes.statusText}`);
        if (!customersRes.ok) throw new Error(`Customers: ${customersRes.statusText}`);
        
        const [ordersData, customersData] = await Promise.all([
          ordersRes.json(),
          customersRes.json()
        ]);
        
        setOrders(ordersData);
        setCustomers(customersData);
      } catch (e: any) {
        setError(String(e));
      } finally {
        setLoading(false);
      }
    }
    
    loadData();
  }, [API]);

  const getCustomerName = (customerId: number) => {
    const customer = customers.find(c => c.id === customerId);
    return customer ? customer.name : `Customer ${customerId}`;
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = !searchQuery || 
      order.status.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.currency.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (order.notes && order.notes.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const matchesStatus = !statusFilter || order.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <main className="main space-y-6">
        <h1 className="h1">Orders</h1>
        <div className="text-center py-8">Loading orders...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="main space-y-6">
        <h1 className="h1">Orders</h1>
        <div className="text-error">{error}</div>
      </main>
    );
  }

  return (
    <main className="main space-y-6">
      <h1 className="h1">Orders</h1>
      
      {/* Filters */}
      <div className="flex gap-4 items-center">
        <div>
          <label className="block text-sm font-medium mb-1">Search</label>
          <input
            type="text"
            placeholder="Search orders..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 w-64"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2"
            aria-label="Filter by order status"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Orders Table */}
      {filteredOrders.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          {orders.length === 0 ? "No orders found" : "No orders match your filters"}
        </div>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Status</th>
              <th>Currency</th>
              <th>Total</th>
              <th>Notes</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{getCustomerName(order.customer_id)}</td>
                <td>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    order.status === 'delivered' ? 'bg-green-100 text-green-800' :
                    order.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                    order.status === 'shipped' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {order.status}
                  </span>
                </td>
                <td>{order.currency}</td>
                <td>{order.total.toFixed(2)}</td>
                <td>{order.notes || "-"}</td>
                <td>{new Date(order.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Summary */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <h3 className="font-medium mb-2">Summary</h3>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Total Orders:</span>
            <span className="ml-2 font-medium">{filteredOrders.length}</span>
          </div>
          <div>
            <span className="text-gray-600">Total Value:</span>
            <span className="ml-2 font-medium">
              {filteredOrders.reduce((sum, order) => sum + order.total, 0).toFixed(2)}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Avg Order Value:</span>
            <span className="ml-2 font-medium">
              {filteredOrders.length > 0 
                ? (filteredOrders.reduce((sum, order) => sum + order.total, 0) / filteredOrders.length).toFixed(2)
                : "0.00"
              }
            </span>
          </div>
        </div>
      </div>
    </main>
  );
}
