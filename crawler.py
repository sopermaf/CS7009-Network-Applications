import requests
import json

destination = "https://api.github.com/users/orangemocha/repos"
response = requests.get(destination)
info = json.loads(response.text)

languages = []

for x in range(0, len(info)):
    languages.append(info[x]['language'])
    
print(languages)


