from neo4jrestclient.client import GraphDatabase
import plotly
from plotly.graph_objs import Scatter, Figure, Layout
import getpass

pw = getpass.getpass()
db = GraphDatabase("http://localhost:7474", username="neo4j", password=pw)

#LANGUAGES VS REPOS
query = "MATCH p=(n)-[r:knows]->() RETURN n.name"
results = db.query(q=query)
knows_count = {}

for result in results:
    username = result[0]
    if username not in knows_count:
        knows_count[username] = 1       #start the count
    elif username in knows_count:
        knows_count[username] += 1      #add count of languages they know

public_repos = []
user_langs = []

#get user repo numbers and format data for graphing
for key, value in knows_count.items():
    #query number of public repos for a particular user
    query = "MATCH (n:`GitHub Users`) Where n.name = '" + key + "' RETURN n.public_repos"
    result = db.query(q=query)
    
    #make the data ready for graphing
    user_langs.append(int(value))
    public_repos.append(int(result[0][0]))   

#AVG NUM OF LANGS PER LOCATION
#1) get the locations
#2)
    
#GRAPH THE DATA
trace0 = Scatter(
    x=user_langs,
    y=public_repos,
    mode='markers'
)
layout = Layout(
    title="Languages Known vs Repo Analysis",
    xaxis=dict(
        range=[0,15],
        title="Number Of Known Languages"
    ),
    yaxis=dict(
        range=[0,200],
        title="Number of Public GitHub Repos"
    )
)

data = [trace0]
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig)


