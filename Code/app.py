import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_clean.csv")
    df['Market'] = df['Market'].str.strip()
    df['Order Region'] = df['Order Region'].str.strip() + " (Region)"
    df['Order Country'] = df['Order Country'].str.strip() + " (Country)"
    df['Order City'] = df['Order City'].str.strip() + " (City)"
    G = nx.read_gml("supply_chain_graph_v3.gml")
    return df, G

df, G = load_data()

markets = ['Africa', 'Europe', 'LATAM', 'Pacific Asia', 'USCA']
regions = [n for n in G.nodes() if "(Region)" in n]
countries = [n for n in G.nodes() if "(Country)" in n]
cities = sorted([n for n in G.nodes() if "(City)" in n])

# --- Topological Sort ---
def kahns_topological_sort(G):
    in_degree = {node: 0 for node in G.nodes()}
    for u, v in G.edges():
        in_degree[v] += 1
    queue = [n for n in G.nodes() if in_degree[n] == 0]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in G.successors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order

topo_order = kahns_topological_sort(G)

# --- Graph Layout ---
def get_positions(G):
    pos = {}
    level_map = {}
    for n in G.nodes():
        if n in markets: level_map[n] = 0
        elif "(Region)" in n: level_map[n] = 1
        elif "(Country)" in n: level_map[n] = 2
        else: level_map[n] = 3

    levels = {}
    for node, lvl in level_map.items():
        levels.setdefault(lvl, []).append(node)

    for lvl, nodes in levels.items():
        for i, node in enumerate(nodes):
            pos[node] = (lvl * 4, i - len(nodes) / 2)
    return pos

pos = get_positions(G)

# --- Draw Graph ---
def draw_graph(G, pos, highlight_path=None, filter_market=None):
    # Filter nodes if market selected
    if filter_market:
        reachable = nx.descendants(G, filter_market) | {filter_market}
        sub = G.subgraph(reachable)
    else:
        sub = G

    edge_x, edge_y = [], []
    for u, v in sub.edges():
        if u in pos and v in pos:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines',
                            line=dict(width=0.3, color='#555'), hoverinfo='none')

    path_traces = []
    if highlight_path:
        for i in range(len(highlight_path) - 1):
            u, v = highlight_path[i], highlight_path[i+1]
            if u in pos and v in pos:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                path_traces.append(go.Scatter(
                    x=[x0, x1, None], y=[y0, y1, None], mode='lines',
                    line=dict(width=4, color='red'), hoverinfo='none'
                ))

    node_x, node_y, node_labels, colors = [], [], [], []
    for n in sub.nodes():
        if n not in pos:
            continue
        node_x.append(pos[n][0])
        node_y.append(pos[n][1])
        node_labels.append(n)
        if highlight_path and n in highlight_path:
            colors.append('red')
        elif n in markets:
            colors.append('#1f77b4')
        elif "(Region)" in n:
            colors.append('#ff7f0e')
        elif "(Country)" in n:
            colors.append('#9467bd')
        else:
            colors.append('#2ca02c')

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=node_labels, textposition='middle right',
        marker=dict(size=6, color=colors),
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace] + path_traces + [node_trace],
        layout=go.Layout(
            showlegend=False, hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=30),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=700
        ))
    return fig

# --- App ---
st.title("Supply Chain Network Optimizer")
st.markdown("Explore the supply chain graph and find optimal shipping routes using real DataCo data.")

tab1, tab2, tab3 = st.tabs(["Supply Chain Graph", "Route Optimizer", "Dataset Explorer"])

# --- Tab 1 ---
with tab1:
    st.subheader("Supply Chain Graph")
    st.markdown("**Blue** = Markets | **Orange** = Regions | **Purple** = Countries | **Green** = Cities")

    filter_market = st.selectbox("Filter by Market (optional)", ["All"] + markets)
    selected = filter_market if filter_market != "All" else None
    fig = draw_graph(G, pos, filter_market=selected)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Topological Processing Order")
    cols = st.columns(4)
    for i, node in enumerate(topo_order):
        cols[i % 4].markdown(f"`{i+1}.` {node}")

# --- Tab 2 ---
with tab2:
    st.subheader("Route Optimizer")
    st.markdown("Find the cheapest or fastest route from a **Market** to a **City**.")

    col1, col2, col3 = st.columns(3)
    with col1:
        source = st.selectbox("Origin (Market)", markets)
    with col2:
        reachable = nx.descendants(G, source)
        reachable_cities = sorted([n for n in reachable if "(City)" in n])
        target = st.selectbox("Destination (City)", reachable_cities)
    with col3:
        optimize_by = st.radio("Optimize for",
                               ["avg_cost", "avg_days"],
                               format_func=lambda x: "Cost" if x == "avg_cost" else "Speed")

    if st.button("Find Best Route"):
        try:
            path = nx.dijkstra_path(G, source, target, weight=optimize_by)
            total = 0
            rows = []
            for i in range(len(path) - 1):
                edge = G[path[i]][path[i+1]]
                w = edge[optimize_by]
                total += w
                rows.append({"From": path[i], "To": path[i+1],
                              optimize_by: round(w, 2)})

            label = "Cost ($)" if optimize_by == "avg_cost" else "Days"
            st.success(f"Optimal path: {' → '.join(path)}")
            st.markdown(f"**Total {label}:** `{round(total, 2)}`")
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

            st.subheader("Route Highlighted on Graph")
            fig2 = draw_graph(G, pos, highlight_path=path)
            st.plotly_chart(fig2, use_container_width=True)

        except nx.NetworkXNoPath:
            st.error(f"No path found from {source} to {target}.")


   
# --- Tab 3 ---
with tab3:
    st.subheader("Dataset Explorer")

    # Use original df without prefixes for charts
    df_raw = pd.read_csv("supply_chain_clean.csv")

    st.markdown("#### Avg Shipping Cost by Market")
    fig3 = px.bar(df_raw.groupby('Market')['Order Item Total'].mean().reset_index(),
                  x='Market', y='Order Item Total',
                  labels={'Order Item Total': 'Avg Cost'}, color='Market')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Delivery Status Distribution")
    delivery_counts = df_raw['Delivery Status'].value_counts().reset_index()
    delivery_counts.columns = ['Status', 'Count']
    fig4 = px.pie(delivery_counts, names='Status', values='Count')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Avg Delivery Days by Shipping Mode")
    fig5 = px.bar(df_raw.groupby('Shipping Mode')['Days for shipping (real)'].mean().reset_index(),
                  x='Shipping Mode', y='Days for shipping (real)',
                  labels={'Days for shipping (real)': 'Avg Days'}, color='Shipping Mode')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("#### Late Delivery Risk by Market")
    fig6 = px.bar(df_raw.groupby('Market')['Late_delivery_risk'].mean().reset_index(),
                  x='Market', y='Late_delivery_risk',
                  labels={'Late_delivery_risk': 'Late Risk Rate'}, color='Market')
    st.plotly_chart(fig6, use_container_width=True)