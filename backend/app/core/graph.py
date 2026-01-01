from typing import Dict, List

class CityGraph:
    GRAPH: Dict[str, Dict[str, float]] = {
        "Warehouse": {"HubA": 3.5, "HubB": 2.8, "TransitX": 4.2},
        "HubA": {"Warehouse": 3.5, "CustomerA": 2.1, "CustomerB": 3.0, "TransitY": 1.8},
        "HubB": {"Warehouse": 2.8, "CustomerC": 2.5, "TransitX": 1.5, "TransitZ": 3.2},
        "TransitX": {"Warehouse": 4.2, "HubB": 1.5, "TransitZ": 2.0, "CustomerD": 3.8},
        "TransitY": {"HubA": 1.8, "CustomerA": 1.2, "CustomerE": 2.7, "DistrictP": 4.0},
        "TransitZ": {"HubB": 3.2, "TransitX": 2.0, "CustomerD": 1.6, "CustomerF": 2.9},
        "CustomerA": {"HubA": 2.1, "TransitY": 1.2, "CustomerB": 1.5},
        "CustomerB": {"HubA": 3.0, "CustomerA": 1.5, "CustomerE": 2.3},
        "CustomerC": {"HubB": 2.5, "CustomerD": 2.8},
        "CustomerD": {"TransitX": 3.8, "TransitZ": 1.6, "CustomerC": 2.8, "CustomerF": 1.9},
        "CustomerE": {"TransitY": 2.7, "CustomerB": 2.3, "DistrictP": 3.5},
        "CustomerF": {"TransitZ": 2.9, "CustomerD": 1.9, "DistrictP": 4.1},
        "DistrictP": {"TransitY": 4.0, "CustomerE": 3.5, "CustomerF": 4.1}
    }
    
    @classmethod
    def get_graph(cls) -> Dict[str, Dict[str, float]]:
        return cls.GRAPH
    
    @classmethod
    def get_nodes(cls) -> List[str]:
        return list(cls.GRAPH.keys())
    
    @classmethod
    def get_edge_count(cls) -> int:
        return sum(len(neighbors) for neighbors in cls.GRAPH.values())
    
    @classmethod
    def node_exists(cls, node: str) -> bool:
        return node in cls.GRAPH
