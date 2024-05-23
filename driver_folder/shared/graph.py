import plotly.graph_objects as go
import networkx as nx

def plot_graph_from_adj_list(adj_list):
    """
    Plots a graph from the given adjacency list using Plotly.

    Parameters:
    adj_list (dict): Adjacency list representation of the graph. 
                     Keys are vertices, values are lists of adjacent vertices.
    
    Example usage:
    adj_list = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }
    plot_graph_from_adj_list(adj_list)
    """
    
    # Create a graph from the adjacency list
    G = nx.Graph(adj_list)
    
    # Create node positions using the spring layout
    pos = nx.spring_layout(G)
    
    # Extract edge information for plotting
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    # Create edge traces
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='none',
        mode='lines')
    
    # Extract node information for plotting
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    # Create node traces
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(G.nodes()),
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='lightblue',
            size=10,
            line_width=2))
    
    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Graph Visualization',
                        title_x=0.5,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))
    
    # Display the plot
    return fig 
    
if __name__ == "__main__":
    

    # Example usage
    adj_list = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }

    plot_graph_from_adj_list(adj_list)
