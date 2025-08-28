## API Endpoints (snapshot)

| Method  | Path |
|---------|------|
| `DELETE` | `/api/v1/customers/{cid}` |
| `DELETE` | `/api/v1/orders/{oid}/items/{iid}` |
| `DELETE` | `/api/v1/orders/{oid}` |
| `DELETE` | `/api/v1/products/{pid}` |
| `DELETE` | `/api/v1/suppliers/{supplier_id}` |
| `GET   ` | `/api/v1/auth/me` |
| `GET   ` | `/api/v1/customers/` |
| `GET   ` | `/api/v1/inventory/products/{product_id}/stock` |
| `GET   ` | `/api/v1/orders/` |
| `GET   ` | `/api/v1/orders/customer/{customer_id}/orders` |
| `GET   ` | `/api/v1/orders/stats/daily` |
| `GET   ` | `/api/v1/orders/stats/summary` |
| `GET   ` | `/api/v1/orders/{oid}/items-summary` |
| `GET   ` | `/api/v1/orders/{oid}/items` |
| `GET   ` | `/api/v1/orders/{oid}` |
| `GET   ` | `/api/v1/products/` |
| `GET   ` | `/api/v1/reports/costs` |
| `GET   ` | `/api/v1/reports/kpis` |
| `GET   ` | `/api/v1/reports/summary` |
| `GET   ` | `/api/v1/suppliers/` |
| `GET   ` | `/api/v1/suppliers/stats` |
| `GET   ` | `/api/v1/suppliers/{supplier_id}` |
| `GET   ` | `/health` |
| `POST  ` | `/api/v1/auth/change-password` |
| `POST  ` | `/api/v1/auth/login` |
| `POST  ` | `/api/v1/auth/logout` |
| `POST  ` | `/api/v1/auth/refresh` |
| `POST  ` | `/api/v1/auth/register` |
| `POST  ` | `/api/v1/customers/` |
| `POST  ` | `/api/v1/inventory/products/{product_id}/adjust` |
| `POST  ` | `/api/v1/inventory/products/{product_id}/release` |
| `POST  ` | `/api/v1/inventory/products/{product_id}/reserve` |
| `POST  ` | `/api/v1/orders/` |
| `POST  ` | `/api/v1/orders/{oid}/items` |
| `POST  ` | `/api/v1/orders/{oid}/status` |
| `POST  ` | `/api/v1/products/` |
| `POST  ` | `/api/v1/reports/refresh` |
| `POST  ` | `/api/v1/suppliers/` |
| `POST  ` | `/api/v1/suppliers/reindex` |
| `POST  ` | `/api/v1/suppliers/upload` |
| `PUT   ` | `/api/v1/customers/{cid}` |
| `PUT   ` | `/api/v1/orders/{oid}/items/{iid}` |
| `PUT   ` | `/api/v1/orders/{oid}` |
| `PUT   ` | `/api/v1/products/{pid}` |
| `PUT   ` | `/api/v1/suppliers/{supplier_id}` |
