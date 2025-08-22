# EPIC-02 / TASK-02K — Deliverables

## Inventory Adjustment (Stock to 10)
```
{"product_id":8,"on_hand":10,"reserved":0,"available":10}```

## Oversell Attempt (409/422 expected)
```
(oversell attempt file not found)
```

## Add/Delete Evidence
```
HTTP/1.1 404 Not Found
date: Fri, 22 Aug 2025 04:00:53 GMT
server: uvicorn
content-length: 22
content-type: application/json

```
```
(delete item file not found)
```

## Totals
```
after_add:
(total_after_add.txt not found)
after_delete:
(total_after_delete.txt not found)
```

## IDs
```
PID=8 CID=3 OID=3
```

## Backend log (last 200)
```
/Users/abdulrahman/Documents/GitHub/shoobydo/apps/backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
INFO:     Started server process [84722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8805 (Press CTRL+C to quit)
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [84722]
```
