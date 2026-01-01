# Customization Guide

## Modify Graph & Add Custom Locations

This guide shows how to customize the network with your own locations and distances.

## Understanding the Graph Structure

The routing network is defined in `backend/app/core/graph.py`.

Each location is a **node**, and distances between them are **edges**.

## Step 1: Add New Locations

### Edit graph.py

```bash
# Open backend/app/core/graph.py
```

### Find the Graph Initialization

Locate:
```python
self.graph = {
    "Warehouse": {"HubA": 3.5, "HubB": 2.8},
    "HubA": {"Warehouse": 3.5, "CustomerA": 2.1, ...},
    # ... more nodes
}
```

### Add a New Location

Example: Add "StoreX" location

```python
self.graph = {
    "Warehouse": {"HubA": 3.5, "HubB": 2.8},
    "HubA": {"Warehouse": 3.5, "CustomerA": 2.1, "StoreX": 4.2},
    "StoreX": {"HubA": 4.2, "CustomerB": 3.1},  # NEW
    # ... rest of graph
}
```

### Update Nodes List

Find:
```python
self.nodes = [
    "Warehouse", "HubA", "HubB", "TransitX",
    "TransitY", "TransitZ", "CustomerA",
    "CustomerB", "CustomerC", "CustomerD",
    "CustomerE", "CustomerF", "DistrictP"
]
```

Add your location:
```python
self.nodes = [
    "Warehouse", "HubA", "HubB", "TransitX",
    "TransitY", "TransitZ", "CustomerA",
    "CustomerB", "CustomerC", "CustomerD",
    "CustomerE", "CustomerF", "DistrictP", "StoreX"  # NEW
]
```

## Step 2: Add Connections (Edges)

### Important Rules

1. **Bidirectional**: If A→B = 3.5, then B→A = 3.5
2. **Symmetric**: Distances must be the same both ways
3. **Distances**: Use realistic km values (can be decimals)
4. **Connectivity**: Each node should connect to at least 1 other node

### Example: Add "DriveWay" Location

```python
self.graph = {
    "Warehouse": {
        "HubA": 3.5,
        "HubB": 2.8,
        "DriveWay": 1.5  # NEW CONNECTION
    },
    "DriveWay": {  # NEW NODE
        "Warehouse": 1.5,
        "CustomerD": 2.3,
        "TransitX": 2.0
    },
    # ... rest of nodes
}
```

Add to nodes list:
```python
self.nodes = [
    # ... existing nodes...,
    "DriveWay"  # NEW
]
```

## Step 3: Test Your Changes

### Restart Backend

```bash
# Stop running backend (Ctrl+C)
# Restart:
cd backend
python run.py
```

### Test New Location

Frontend should now show "StoreX" and "DriveWay" in dropdowns.

Test API:
```bash
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "StoreX"}'
```

## Real-World Example: Add Delhi Locations

### New Locations:
- CGO Complex
- Aerocity
- Noida City Center

### Implementation:

```python
self.graph = {
    "Warehouse": {
        "HubA": 3.5,
        "HubB": 2.8,
        "CGO_Complex": 2.1  # NEW
    },
    "CGO_Complex": {  # NEW NODE
        "Warehouse": 2.1,
        "Aerocity": 3.2,
        "CustomerC": 1.8
    },
    "Aerocity": {  # NEW NODE
        "CGO_Complex": 3.2,
        "Noida_City_Center": 4.5,
        "HubA": 2.9
    },
    "Noida_City_Center": {  # NEW NODE
        "Aerocity": 4.5,
        "CustomerE": 2.1,
        "CustomerF": 2.8
    },
    # ... rest of graph
}

self.nodes = [
    "Warehouse", "HubA", "HubB", "TransitX",
    "TransitY", "TransitZ", "CustomerA",
    "CustomerB", "CustomerC", "CustomerD",
    "CustomerE", "CustomerF", "DistrictP",
    "CGO_Complex", "Aerocity", "Noida_City_Center"  # NEW
]
```

## Step 4: Update Frontend (Optional)

Frontend automatically detects new locations from the backend.

No frontend changes needed!

## Best Practices

### 1. Naming Conventions

Use consistent naming:
- ✅ "CustomerA", "CustomerB" (good)
- ❌ "customer_a", "CUSTOMER_A" (inconsistent)
- ✅ "CGO_Complex", "Noida_City_Center" (descriptive)
- ❌ "loc1", "place2" (unclear)

### 2. Distance Accuracy

```python
# Good: Realistic distances
"Warehouse": {"HubA": 3.5, "CustomerA": 8.2}

# Bad: Unrealistic values
"Warehouse": {"HubA": 1000, "CustomerA": 0.01}
```

### 3. Bidirectional Edges

```python
# ✅ CORRECT - Both directions have same distance
"LocationA": {"LocationB": 5.0},
"LocationB": {"LocationA": 5.0},

# ❌ WRONG - Asymmetric distances
"LocationA": {"LocationB": 5.0},
"LocationB": {"LocationA": 7.0},  # Should be 5.0!
```

### 4. Connectivity

Ensure all nodes are reachable:

```python
# Good: Well connected
"NewLocation": {
    "HubA": 3.0,
    "HubB": 2.5,
    "TransitX": 1.8
}

# Bad: Only one connection
"IsolatedLoc": {
    "OnlyHub": 5.0  # Can't reach other locations efficiently
}
```

## Batch Customization: Add 5 Locations

### Current: 13 nodes
### Goal: Add 5 new locations (Punjabi Bagh, Safdarjung, Gurgaon, Faridabad, Noida)

### Code Template

```python
self.graph = {
    # EXISTING
    "Warehouse": {...},
    # ... existing nodes ...
    
    # NEW LOCATIONS
    "Punjabi_Bagh": {
        "Warehouse": 2.5,
        "HubA": 1.8,
        "CustomerA": 3.2,
        "Safdarjung": 2.1
    },
    "Safdarjung": {
        "Punjabi_Bagh": 2.1,
        "HubB": 2.4,
        "CustomerB": 1.9,
        "Gurgaon": 3.5
    },
    "Gurgaon": {
        "Safdarjung": 3.5,
        "Faridabad": 4.2,
        "CustomerC": 2.8
    },
    "Faridabad": {
        "Gurgaon": 4.2,
        "Noida": 3.1,
        "CustomerD": 3.5
    },
    "Noida": {
        "Faridabad": 3.1,
        "Warehouse": 4.0,
        "CustomerE": 2.2
    }
}

self.nodes = [
    "Warehouse", "HubA", "HubB", "TransitX",
    "TransitY", "TransitZ", "CustomerA",
    "CustomerB", "CustomerC", "CustomerD",
    "CustomerE", "CustomerF", "DistrictP",
    "Punjabi_Bagh", "Safdarjung", "Gurgaon",
    "Faridabad", "Noida"
]
```

## Verification

After customization:

```bash
# Check node count increased
curl http://localhost:8000/api/v1/graph
# Should show: "total_nodes": 18 (if added 5 locations)

# Test routes to new locations
curl -X POST http://localhost:8000/api/v1/route \
  -H "Content-Type: application/json" \
  -d '{"start": "Warehouse", "end": "Punjabi_Bagh"}'
```

## Troubleshooting Customization

### Error: "Location not found"

Check:
1. Location name spelling (case-sensitive)
2. Location added to `self.nodes` list
3. Backend restarted

### Error: "No route found"

Check:
1. Both locations connected in graph
2. No isolated nodes
3. Graph is bidirectional

### Performance Issue

Too many locations might slow routing:
- Keep < 100 locations for best performance
- Use indexed locations for large networks

## Export Your Configuration

Save your graph as JSON:

```bash
python -c "from app.core.graph import LogisticsGraph; import json; g = LogisticsGraph(); print(json.dumps(g.graph, indent=2))" > graph_backup.json
```

---

**Your logistics network is now fully customized!** 🗺️
