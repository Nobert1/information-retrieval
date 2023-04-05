#  Install the Python Requests library:
# `pip install requests`
import requests
import json

api_key = "S3VTYQM6NL93P0J2F2ECR51UR2SXDS4VQOL8XWTLAJMLBZJBMW4J822IQ3F25154B32P5DRNR378L3EF"
child_mode_on = False

f = open("adult_queries/bing.json" , "rb" )
results = json.load(f)
f.close()

results_copy = results

def send_request(query):
    params = {}
    if child_mode_on:
        params = {
            "api_key": api_key,
            "search": query,
            "add_html": True,
            "nb_results": 10,
            "extra_params": "safe=active"
        }
    else:
        params = {
            "api_key": api_key,
            "search": query,
            "add_html": True,
            "nb_results": 10,
        }

    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/store/google",
        params=params,
    )
    content_as_json = json.loads(response.content)
    
    resultsList = []
    if "organic_results" in content_as_json:
        for result in content_as_json['organic_results']:
            results_obj = {"url": result['url'], "description": result["description"]}
            resultsList.append(results_obj)
    
    results_copy[query]["results"] = resultsList
    with open("data/adults_results.json", "w") as fp:
        json.dump(results_copy , fp)
    
for key, dict in results.items():
    send_request(key)


