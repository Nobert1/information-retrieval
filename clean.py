import json
f = open("data/child_results.json" , "rb" )
queries = json.load(f)
f.close()

duplicate_dict = queries
for key, query in queries.items():
    for result_key in ["results", "bing_results"]:
        result_list = []
        for result in query[result_key]:
            duplicate_result = result
            if "html_text" in duplicate_result:
                del duplicate_result["html_text"]
            result_list.append(duplicate_result)
            result_list.append(duplicate_result)
        query[key] = {}
        query[key][result_key] = result_list

with open("data/serp_results.json", "w", encoding="utf-8") as fp:
    json.dump(duplicate_dict , fp, ensure_ascii=False)
