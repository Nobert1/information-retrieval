#  Install the Python Requests library:
# `pip install requests`
import requests
import urllib.parse
import json

f = open("kids_queries/kids_queries_dataset_classified_with_grades.json" , "rb" )
jsonObject = json.load(f)
f.close()

queries = []
i = 0
for object in jsonObject:
    queries.append(object["queries"])
    i += 1
    if i > 10:
        break

results = {}

def send_request(search_keywords):
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/store/google",
        params={
            "api_key": "MFKWOPYWBKVMDJ05EL9K75BAVBVWJ40WKR2ZURMVKLA3E16VH94Q34EAADLC1LGGMH91N8N6LYG4LQRJ",
            "search": search_keywords,
            "add_html": True,
            "nb_results": 10,
            "extra_params": "safe=active"
        },
    )
    content_as_json = json.loads(response.content)
    
    resultsList = []
    if "organic_results" in content_as_json:
        for result in content_as_json['organic_results']:
            obj = {"url": result['url'], "description": result['description'], "actual_grade": result['Grade']}
            resultsList.append(obj)
    
    results[search_keywords] = resultsList
       
for query in queries:
    send_request(query)

with open("childs_results", "w") as fp:
    json.dump(results , fp)
