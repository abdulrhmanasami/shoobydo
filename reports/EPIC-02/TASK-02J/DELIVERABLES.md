]633;E;{ echo "# EPIC-02 / TASK-02J \xffffffffffffffe2\xffffffffffffff80\xffffffffffffff93 Deliverables"\x3b echo\x3b echo "## 1) curl_01_add_items.txt (first 40 lines)"\x3b echo '```http'\x3b head -n 40 reports/EPIC-02/TASK-02J/curl_01_add_items.txt\x3b echo '```'\x3b echo\x3b echo "## 2) available_paths (first 30 lines)"\x3b echo '```text'\x3b sed -n '1,30p' reports/EPIC-02/TASK-02J/available_paths.txt\x3b echo '```'\x3b echo\x3b echo "## 3) PR link"\x3b cat reports/EPIC-02/TASK-02J/pr_link.txt\x3b } > reports/EPIC-02/TASK-02J/DELIVERABLES.md;]633;C# EPIC-02 / TASK-02J – Deliverables

## 1) curl_01_add_items.txt (first 40 lines)
```http
HTTP/1.1 200 OK
date: Fri, 22 Aug 2025 02:40:52 GMT
server: uvicorn
content-length: 65
content-type: application/json

{"product_id":8,"qty":2,"unit_price":10.0,"id":1,"subtotal":20.0}```

## 2) available_paths (first 30 lines)
```text
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
https://github.com/abdulrhmanasami/shoobydo/pull/6
