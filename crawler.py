import requests
import json
import datetime
import time

file = open("names.txt", 'w')

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
    get_rate = "https://api.github.com/rate_limit"
    wait_info = json.loads(requests.get(get_rate).text)
    req_remaining = wait_info['resources']['core']['remaining']
    req_remaining = int(req_remaining)
    
    if req_remaining > 5:
        return
    
    reset = wait_info['resources']['core']['reset']
    time_reset = datetime.datetime.fromtimestamp(reset)
    wait_time_sec = reset - time.time()
    
    print("\nSleeping for", round(wait_time_sec/60), "mins...")
    print("Waking at", time_reset)
    time.sleep(wait_time_sec)
    print("Sleep ended..\n")
    
def searchUser(user):
    #get repos
    wait_check()
    response1 = requests.get(userRepoURL(user))             #request 1
    user_repo_info = json.loads(response1.text)
    
    #stats from user
    print("CURRENT USER:", user)
    found_users.append(user)
    file.write(user + "\n")             #write stats to file
    
    #process repos
    for repo in user_repo_info:
    
        #access the list of contributors for that repo
        wait_check()
        contrib_response = requests.get(repo['contributors_url'])       #request 2
        contrib_info = json.loads(contrib_response.text)
        for contributor in contrib_info:
            contrib_username = contributor['login']
            if contrib_username != user:
                searchUser(contrib_username)

    
current_user = "GrahamCampbell"
searchUser(current_user)
print("LIST OF USERS FOUND:", found_users)

#wait_check()

#file.close()