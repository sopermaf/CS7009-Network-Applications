from neo4jrestclient.client import GraphDatabase
import requests
import json
import datetime
import time
import getpass

found_users = []
users_to_search = []

#dictionaries of data nodes and their names
user_nodes = {}
location_nodes = {}
repo_nodes = {}
language_nodes = {}

pw = getpass.getpass()
db = GraphDatabase("http://localhost:7474", username="neo4j", password=pw)
user_label = db.labels.create("GitHub Users")
location_label = db.labels.create("GitHub Locations")
repo_label = db.labels.create("GitHub Repositories")
language_label = db.labels.create("Programming Languages")

KEEP_REQ = 1       #keeps a set number of requests left within your limit for manual use

def userRepoURL(user):
    return "https://api.github.com/users/" + user + "/repos"
    
#need to check if I will go over limit of requests
def wait_check():
    get_rate = "https://api.github.com/rate_limit"
    wait_info = json.loads(requests.get(get_rate).text)
    req_remaining = wait_info['resources']['core']['remaining']
    req_remaining = int(req_remaining)
    
    if req_remaining > KEEP_REQ:
        return
    
    reset = wait_info['resources']['core']['reset']
    time_reset = datetime.datetime.fromtimestamp(reset)
    wait_time_sec = reset - time.time()
    
    print("\nSleeping for", round(wait_time_sec/60), "mins...")
    print("Waking at", time_reset)
    time.sleep(wait_time_sec+20)
    
    print("Sleep ended..\n")

#recursive
def searchUser(user):
    #get repos
    wait_check()
    response1 = requests.get(userRepoURL(user))             #request 1
    user_repo_info = json.loads(response1.text)
    
    #stats from user
    print("CURRENT USER:", user)
    found_users.append(user)
    langs = repoLanguages(user_repo_info)
    
    #write the info to a file
    file = open("names_lang.txt", 'a+')           #append mode
    file.write("\n" + str(user))
    for lang in langs:
        file.write(" " + str(lang))
    file.close()
    
    time.sleep(30)   #30 second sleep due to github limits
    
    #process repos
    for repo in user_repo_info:
        #access the list of contributors for that repo
        wait_check()
        contrib_response = requests.get(repo['contributors_url'])       #request 2
        contrib_info = json.loads(contrib_response.text)
        for contributor in contrib_info:
            contrib_username = contributor['login']
            if contrib_username not in found_users:     #avoid wasted requests on previously found users
                searchUser(contrib_username)

#gets user info from api and adds a node
def makeUser(user):
    if user in user_nodes:  #save requests and avoid duplication
        return
    
    wait_check()
    user_request_addr = "https://api.github.com/users/" + user
    response1 = requests.get(user_request_addr)             
    user_json = json.loads(response1.text)
    
    username = user_json['login']
    location = user_json['location']
    
    #user node made
    user_nodes[username] = db.nodes.create(username=user_json['login'], name=user_json['name'], company=user_json['company'],
    hireable = user_json['hireable'], public_repos=user_json['public_repos'], bio=user_json['bio'],
    email=user_json['email'], num_followers=user_json['followers'], num_following=user_json['following'])
    user_label.add(user_nodes[username])
    
    #location node made
    if location not in location_nodes:      #avoid duplication
        location_nodes[location] = db.nodes.create(location_name=location)
        location_label.add(location_nodes[location])
        
    #link user with location
    user_nodes[username].relationships.create("lives in", location_nodes[location])
     
#iterative method
def search_userList(user):
    wait_check()        #avoid bad request
    
    #POSSIBLE TO CHECK IF THEY HAVE A REPO FIRST???
    response1 = requests.get(userRepoURL(user))
    user_repo_info = json.loads(response1.text)  
    
    for repo in user_repo_info:
        #add the repo node
        repo_nm = repo['name']
        repo_lang = repo['language']
        repo_nodes[repo_nm] = db.nodes.create(name=repo_nm, size=repo['size'], watchers=repo['watchers'], stargazers=repo['stargazers_count'], homepage=repo['homepage'])
        repo_label.add(repo_nodes[repo_nm])
        
        #relationships with owner for repo and lang
        if repo_lang not in language_nodes:
            language_nodes[repo_lang] = db.nodes.create(lang_name=repo_lang)
            language_label.add(language_nodes[repo_lang])
            
        #relationships with owner
        user_nodes[user].relationships.create("knows", language_nodes[repo_lang])
        user_nodes[user].relationships.create("owns", repo_nodes[repo_nm])
        user_nodes[user].relationships.create("contributes", repo_nodes[repo_nm])
        
        #access the list of contributors for that repo
        wait_check()            #avoid bad request
        contrib_response = requests.get(repo['contributors_url'])       #request 2
        contrib_info = json.loads(contrib_response.text)
        
        for contributor in contrib_info:
            contrib_username = contributor['login']
            makeUser(contrib_username)  #add the user info and links location, method avoids duplication as well
            
            #add relationships for contributor
            user_nodes[contrib_username].relationships.create("contributes", repo_nodes[repo_nm])
            user_nodes[contrib_username].relationships.create("knows", language_nodes[repo_lang])
            
            if contrib_username not in users_to_search:
                users_to_search.append(contrib_username)    #add them for future search in the loop
    
top_user = "GrahamCampbell"
second_user = "fabpot"
third_user = "weierophinney"
guy_from_lecture = "afc163"
interesting = "google"

users_to_search.append(second_user)

#done iteratively to avoid recursive depth limit
count = 0
for user_next in users_to_search:
    makeUser(user_next)
    search_userList(user_next)
    print("Currently on index", count, "of", len(users_to_search))
    count += 1