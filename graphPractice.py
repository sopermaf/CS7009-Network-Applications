import plotly
from plotly.graph_objs import Scatter, Figure, Layout

values = [195, 112, 150]
labels = ['Python', 'Java', 'HTML']


fig = {
    'data': [{'labels': labels,
              'values': values,
              'type': 'pie'}],
    'layout': {'title': 'GitHub Repository Languages Found'}
     }

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='markers',
    marker=dict(
        size=[40, 60, 80, 100],
    )
)
data = [trace0]

# plotly.offline.plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])])

plotly.offline.plot(fig)
plotly.offline.plot(data)