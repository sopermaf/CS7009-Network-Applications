from neo4jrestclient.client import GraphDatabase
import getpass

pw = getpass.getpass()
db = GraphDatabase("http://localhost:7474", username="neo4j", password=pw)

users = []
user_langs = []
unique_lang = []
lang_nodes = []

file = open("names_lang1.txt", 'r')
flines = file.readlines()
for line in flines:
    line_info = line.split()
    users.append(line_info[0])  #username always first
    
    curr_user_langs = []
    for curr in range(1, len(line_info)):   
        curr_lang = line_info[curr]
        curr_user_langs.append(curr_lang)
        if curr_lang not in unique_lang:
            unique_lang.append(curr_lang)
            lang_nodes.append(db.nodes.create(name=str(curr_lang)))          #create node of that language
            
    user_langs.append(curr_user_langs)
    
file.close()

#create nodes for the languages
lang_db = db.labels.create("Programming Languages")
for node in lang_nodes:
    lang_db.add(node)       #add each node
    
    
#create user nodes and link to the language nodes
users_db = db.labels.create("GitHub User")
for i in range(0, len(users)):
    new_user_node = db.nodes.create(name=str(users[i]))
    
    #add relationships from user to lang
    for lang in user_langs[i]:
        lang_index = unique_lang.index(lang)
        new_user_node.relationships.create("knows", lang_nodes[lang_index])
    
    users_db.add(new_user_node)