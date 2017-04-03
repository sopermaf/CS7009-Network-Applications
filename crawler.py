import requests
import json
import datetime

def numUniqueLang(languages):
    uniq = []
    for lang in languages:
        if lang not in uniq:
            uniq.append(lang)
    
    print(uniq)
    return len(uniq)

def userRepoURL(user):
    return "https://api.github.com/users/" + user + "/repos"

found_users = []

#need to check if I will go over limit of requests
def wait_check():
    pass

def searchUser(user):
    #get repos
    response1 = requests.get(userRepoURL(user))
    user_repo_info = json.loads(response1.text)
    
    #stats from repos
    print("CURRENT USER:", user)
    found_users.append(user)
    
    #process repo
    for repo in user_repo_info:
        contrib_response = requests.get(repo['contributors_url'])
        contrib_info = json.loads(contrib_response.text)
        
        #process each contributor to that repo
        for contributor in contrib_info:
            contrib_username = contributor['login']
            if contrib_username != user:
                searchUser(user)

    
current_user = "GrahamCampbell"
searchUser(current_user)
print("LIST OF USERS FOUND:", found_users)


