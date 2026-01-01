# API Testing Guide

## Comprehensive Testing Instructions

This guide covers all methods to test the Smart Logistics Routing Engine.

## Test Environment Setup

Before testing, ensure:
1. Backend running: `python run.py` (Port 8000)
2. Frontend running: `python -m http.server 3000` (Port 3000)
3. Both terminals open and showing no errors

## Test 1: Web UI Testing

### Basic Route Calculation

1. Open browser: **http://localhost:3000**
2. Select Start Location: **Warehouse**
3. Select End Location: **CustomerE**
4. Click **Calculate Route**
5. Observe:
   - Path appears with arrows
   - Distance shown
   - Nodes visited displayed

### Test All Locations

Test these routes:

```
Warehouse → CustomerA   (shortest)
Warehouse → DistrictP   (longest)
HubA → CustomerF
HubB → TransitX
```

### Error Handling

1. Try invalid locations
2. Try same start/end
3. Clear selections

## Test 2: API Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected 200 OK:
```json
{
  "status": "healthy",
  "service": "Smart Logistics Routing Engine",
  "version": "1.0.0"
}
```

## Test 3: Get Graph Information

```bash
curl http://localhost:8000/api/v1/graph
```

Expected response:
```json
{
  "nodes": [
    "Warehouse", "HubA", "HubB", "TransitX",
    "TransitY", "TransitZ", "CustomerA",
    "CustomerB", "CustomerC", "CustomerD",
    "CustomerE", "CustomerF", "DistrictP"
  ],
  "total_nodes": 13,
  "total_edges": 40
}
```

## Test 4: Calculate Routes via API

### Test 4.1: Simple Route

```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "CustomerE"}'
```

Expected:
```json
{
  "path": ["Warehouse", "HubA", "CustomerE"],
  "distance": 8.5,
  "nodes_visited": 5,
  "success": true
}
```

### Test 4.2: Multiple Routes

```bash
# Route 1
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "DistrictP"}'

# Route 2
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "HubA", "end": "CustomerF"}'

# Route 3
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "TransitX", "end": "CustomerB"}'
```

### Test 4.3: Error Cases

#### Invalid Location

```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "InvalidCity", "end": "CustomerE"}'
```

Expected 404:
```json
{
  "detail": "Start location 'InvalidCity' not found in network"
}
```

#### Missing Field

```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse"}'
```

Expected 422 Validation Error

#### Empty Request

```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected 422 Validation Error

## Test 5: Using Postman

1. Open Postman
2. Create POST request
3. URL: `http://localhost:8000/api/v1/route`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
```json
{"start": "Warehouse", "end": "CustomerE"}
```
6. Send and check response

## Test 6: Using Python Requests

```python
import requests

url = "http://localhost:8000/api/v1/route"
payload = {"start": "Warehouse", "end": "CustomerE"}

response = requests.post(url, json=payload)
print(response.json())
```

## Test 7: Performance Testing

### Response Time

```bash
time curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "DistrictP"}'
```

Should complete in < 10ms

### Load Testing with Apache Bench

```bash
ab -n 100 -c 10 \
  -p data.json \
  -T application/json \
  http://localhost:8000/api/v1/route
```

## Test 8: API Documentation

1. Open: **http://localhost:8000/api/docs**
2. Interactive Swagger UI
3. Try requests directly in browser
4. See request/response examples

## Test 9: Available Locations

Test with all these locations:

```
✓ Warehouse
✓ HubA
✓ HubB
✓ TransitX
✓ TransitY
✓ TransitZ
✓ CustomerA
✓ CustomerB
✓ CustomerC
✓ CustomerD
✓ CustomerE
✓ CustomerF
✓ DistrictP
```

## Test Results Checklist

- [ ] Health check returns 200
- [ ] Graph endpoint returns 13 nodes
- [ ] Web UI displays correctly
- [ ] Route calculation works
- [ ] Distance is accurate
- [ ] Path shows correct sequence
- [ ] Invalid location returns 404
- [ ] Missing field returns 422
- [ ] Response time < 10ms
- [ ] API docs work
- [ ] All 13 locations accessible

## Troubleshooting Tests

### Connection Refused

```
Error: Connection refused on localhost:8000
```

**Solution**: Backend not running
```bash
cd backend
python run.py
```

### 404 Not Found

```
Error: 404 Client Error: Not Found
```

**Solution**: Check location spelling (case-sensitive)

### 422 Validation Error

```
422 Unprocessable Entity
```

**Solution**: Missing required fields in JSON

## Success Indicators

✅ All endpoints return HTTP 200  
✅ Responses are valid JSON  
✅ Paths are logical  
✅ Distances are positive  
✅ Error messages are clear  
✅ Response times are fast  

---

Your Smart Logistics Engine is fully tested and ready! 🎉
