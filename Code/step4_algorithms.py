import networkx as nx

G = nx.read_gml("supply_chain_graph_v3.gml")

def find_best_route(G, source, target, weight_by="avg_cost"):
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_by)
        total = 0
        print(f"\nBest route ({weight_by}): {source} -> {target}")
        for i in range(len(path) - 1):
            edge = G[path[i]][path[i+1]]
            w = edge[weight_by]
            total += w
            print(f"  {path[i]} -> {path[i+1]} | {weight_by}: {w}")
        print(f"  TOTAL {weight_by}: {round(total, 2)}")
        return path
    except nx.NetworkXNoPath:
        print(f"No path from {source} to {target}")
        return []

# Test runs
find_best_route(G, "Europe", "Paris (City)", weight_by="avg_cost")
find_best_route(G, "USCA", "Toronto (City)", weight_by="avg_days")
find_best_route(G, "Pacific Asia", "Tokyo (City)", weight_by="avg_cost")