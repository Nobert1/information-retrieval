#  Install the Python Requests library:
# `pip install requests`
import requests
import json

f = open("kids_queries/kids_queries_dataset_classified_with_grades.json" , "rb" )
jsonObject = json.load(f)
f.close()
api_key = "315AL9D0VKT4ATHOYVZ5E3OH98V4MG1K6M9XYTUEZWZY496KDIJ51J59R7QWG7VDDHVADOFA5MNJPAP4"
child_mode_on = True
query_dicts = []
i = 11

for object in jsonObject:
    if(i > 10):
        query_dicts.append(object)
    i += 1
    if i > 50:
        break

f = open("data/childs_results2.json" , "rb" )
results = json.load(f)
f.close()

def send_request(query_dict):
    params = {}
    if child_mode_on:
        params = {
            "api_key": api_key,
            "search": query_dict["queries"],
            "add_html": True,
            "nb_results": 10,
            "extra_params": "safe=active"
        }
    else:
        params = {
            "api_key": api_key,
            "search": query_dict["queries"],
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
    
    query_dict["results"] = resultsList
    results[query_dict["queries"]] = query_dict
    with open("data/adults_results.json", "w") as fp:
        json.dump(results , fp)
    
for query_dict in query_dicts:
    send_request(query_dict)


