## utilizes azure to search bing.

#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-
# from IPython.display import HTML
import json
import requests

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = ""
search_url = "https://api.bing.microsoft.com/v7.0/search"
endpoint = search_url + "/bing/v7.0/search"

f = open("" , "rb" )
dataset = json.load(f)
f.close()
child_mode_on = False
# Query term(s) to search for. 

# Construct a request
mkt = 'en-US'
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
search_term = "Microsoft Bing Search Services"
# Call the API
dataset_copy = {}
for data_object in dataset: #.items()
    try:
        query = data_object["queries"]
        params = {}
        dataset_copy[query] = {"queries": query}
        # dataset_copy[data_object["queries"]][data_object["queries"]] = data_object["queries"]
        if child_mode_on:
            params = { 'q': query, 'mkt': mkt, 'safe-search': 'strict' }
        else:
            params = { 'q': query, 'mkt': mkt }

        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        for _, result in search_results.items():
            result_list = []
            for webpage in search_results["webPages"]["value"]:
                if webpage:
                    result_list.append({"url": webpage["url"], "description": webpage["snippet"]})
            dataset_copy[query]["bing_results"] = result_list
            with open("", "w") as fp:
                json.dump(dataset_copy , fp)

    except Exception as ex:
        raise ex

