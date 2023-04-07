## transforms the readnet scores into grades and compares them with the grades of the children conducting the query.

import os
import pandas as pd
def get_readnet_grade(readnet_score):
    if readnet_score < 2: 
        return 3 ## 3,8
    if readnet_score < 3: 
        return 4 ## 4,9
    if readnet_score < 4:
        return 5 ## 5,10
    if readnet_score < 4.25:
        return 6 ## 6,11
    if readnet_score < 4.50:
        return 7 ## 7,12
    if readnet_score < 4.75:     
        return 8 ## 8,13
    if readnet_score < 5:
        return 9 ## 9,14
    if readnet_score < 5.25:
        return 10 ## 10,15
    if readnet_score < 5.50:
        return 11 ## 10,16
    if readnet_score < 5.75:
        return 11 ## 10,17
    return 13 ## 18

if __name__ == "__main__":
    result_readable = {}
    queries = pd.read_json(f"data/child.json")
    queries_copy = queries
    for search_engine in ["results", "bing_results"]:
        only_website = 0
        only_description = 0
        n_website = 0
        n_desc = 0
        for key, query in queries.items():
            if search_engine in query:
                result_page = query[search_engine]
                for result in result_page:
                    description_readable = False
                    website_readable = False
                    if "ReadNet_score_description" in result:
                        grade = get_readnet_grade(result["ReadNet_score_description"])
                        n_desc += 1
                        description_readable = grade <= query["Grade"]
                    if "ReadNet_score_html_text" in result:
                        grade = get_readnet_grade(result["ReadNet_score_html_text"])
                        n_website += 1
                        website_readable = grade <= query["Grade"]
                    if description_readable:
                        only_description += 1
                    if website_readable:
                        only_website += 1
        print("search engine: " + search_engine)
        print("only_website", only_website, " n_website ", n_website)
        print("only_description: ", only_description, " n_desc ", n_desc)
        print("\n")
                
                    
    
                 



adult_readnet_scores = {}
