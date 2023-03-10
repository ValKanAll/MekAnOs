import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""Uses plotly to show meshes in web browsers"""

def add_points2graph(figure, points, legend=None, size=1, row=None, col=None):
    """
    Adds mesh to a plotly graph
    :param figure: plotly Figure object
    :param points: point list
    :return: nothing, just plots the mesh on the plotly figure
    """
    show_at_the_end = False
    if not figure:
        show_at_the_end = True
        layout = go.Layout(scene=dict(aspectmode='data'))  # equal scale step
        figure = go.Figure(layout=layout)

    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    marker_data = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        marker=go.scatter3d.Marker(size=size),
        opacity=0.8,
        mode='markers',
        name=legend
    )
    if row and col:
        figure.add_trace(marker_data, row=row, col=col)
    else:
        figure.add_trace(marker_data)

    if show_at_the_end:
        figure.show()
