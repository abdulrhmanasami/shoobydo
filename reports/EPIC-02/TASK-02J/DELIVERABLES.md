# EPIC-02 / TASK-02J — Deliverables

## 1) head -n 40 curl_01_add_items.txt
```
HTTP/1.1 200 OK
date: Fri, 22 Aug 2025 02:40:52 GMT
server: uvicorn
content-length: 65
content-type: application/json

{"product_id":8,"qty":2,"unit_price":10.0,"id":1,"subtotal":20.0}```

## 2) available_paths (أول 30 سطر)
```
"/api/health"
"/api/v1/auth/login"
"/api/v1/auth/logout"
"/api/v1/auth/refresh"
"/api/v1/auth/register"
"/api/v1/customers/"
"/api/v1/customers/{cid}"
"/api/v1/orders/"
"/api/v1/orders/{oid}"
"/api/v1/orders/{oid}/items"
"/api/v1/orders/{oid}/items/{iid}"
"/api/v1/products/"
"/api/v1/products/{pid}"
```

## 3) PR link
```
https://github.com/abdulrhmanasami/shoobydo/pull/6
```

—
ENV: PORT=8805
Commit: 84547ee
Health: {"ok":true}
