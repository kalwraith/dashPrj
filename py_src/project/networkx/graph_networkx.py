from py_src.project.networkx.run_apriori import RunApriori
import networkx as nx
import plotly.graph_objects as go


class GraphNetworkx():
    def __init__(self, apriori_rslt_df, layout):
        self.layout =layout
        self.apriori_rslt_df = apriori_rslt_df
        self.set_networkx()

    def set_networkx(self):
        self.G = nx.Graph()
        self.G.add_edges_from(self.apriori_rslt_df['itemsets'].tolist())

        if self.layout == 'circular':
            self.pos = nx.layout.circular_layout(self.G)        #self.pos 는 딕셔너리 구조임 ({'수사': array([ 0.18898969, -0.63194547])...})
        elif self.layout == 'kamada_kawai':
            self.pos = nx.layout.kamada_kawai_layout(self.G)
        elif self.layout == 'fruchterman_reingold':
            self.pos = nx.layout.fruchterman_reingold_layout(self.G)
        elif self.layout == 'random':
            self.pos = nx.layout.random_layout(self.G)
        elif self.layout == 'shell':
            self.pos = nx.layout.shell_layout(self.G)
        elif self.layout == 'spectral':
            self.pos = nx.layout.spectral_layout(self.G)
        elif self.layout == 'spiral':
            self.pos = nx.layout.spiral_layout(self.G)

        return self.G, self.pos

    def get_edge_scatter(self):
        edge_x = []
        edge_y = []
        for edge in self.G.edges():     #edge는 ('수사', '검찰'),('수사', '경찰')... 같은 set 구조임
            edge_x.append(self.pos[edge[0]][0])
            edge_y.append(self.pos[edge[0]][1])
            edge_x.append(self.pos[edge[1]][0])
            edge_y.append(self.pos[edge[1]][1])
            edge_x.append(None)
            edge_y.append(None)
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        return edge_trace

    def get_node_scatter(self):
        node_x = []
        node_y = []
        for pos_lst in self.pos.values():
            node_x.append(pos_lst[0])
            node_y.append(pos_lst[1])


        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(self.G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(f'{adjacencies[0]} (connections: {str(len(adjacencies[1]))})')

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        return node_trace


    def get_networkx_fig(self):
        fig = go.Figure(data=[self.get_edge_scatter(), self.get_node_scatter()],
                        layout=go.Layout(
                            title='<br>Network graph made with Python',
                            #titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text='',
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        return fig

# run_apriori = RunApriori('201903')
# graph_networkx = GraphNetworkx(run_apriori.get_apriori_rslt(min_support=0.02))
# graph_networkx.set_networkx()