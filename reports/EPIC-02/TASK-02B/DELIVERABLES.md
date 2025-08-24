# EPIC-02 / TASK-02B — Deliverables
## 1) suppliers list (HTTP head)
```
HTTP/1.1 200 OK
date: Sun, 24 Aug 2025 11:56:11 GMT
server: uvicorn
content-length: 275
content-type: application/json

[{"id":1,"name":"Test Supplier","file_path":"/test/path.xlsx","rows":100,"sheets":2},{"id":2,"name":"Test Supplier 2","file_path":"/test/path2.xlsx","rows":200,"sheets":3},{"id":3,"name":"Deliverable Test Supplier","file_path":"/deliverable/test.xlsx","rows":150,"sheets":2}]```
## 2) available_paths (suppliers)
```
/api/v1/suppliers/
/api/v1/suppliers/reindex
/api/v1/suppliers/stats
/api/v1/suppliers/upload
/api/v1/suppliers/{supplier_id}
```
## 3) backend log tail (last 200)
```
INFO:     Started server process [88303]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8805 (Press CTRL+C to quit)
```
