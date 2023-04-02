import json
import requests
from bs4 import BeautifulSoup
import re

f = open("data/childs_results.json" , "rb" )
queries = json.load(f)
f.close()
i = 10

def remove_tags(html):
 
    # parse html content
    string = html.decode('utf-8')
    html = string.encode('utf-8', 'ignore')
    html = html.decode('utf-8')

    words = html.split()
    # Keep only words with English characters
    html = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]
    # Join the English words back into a string
    html = ' '.join(html)
    soup = BeautifulSoup(html, "html.parser")#.get_text(strip=True)
    [s.extract() for s in soup(['iframe', 'script', 'style'])]
    # return soup.find_all(text=True)
    soup.encode("utf-8")
 
    # # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

duplicate_dict = {}

for search_query in queries:
    print("search_query", search_query)
    result_list = []
    for result in queries[search_query]:
        duplicate_result = result
        try:
            url = result["url"]
            response = requests.get(url, timeout=2000)
            if response.status_code > 299:
                result_list.append(duplicate_result)
                break
            html_content = response.content
            cleaned_body = remove_tags(html_content)
            duplicate_result["html_text"] = cleaned_body
        except:
            print("error occured")
        result_list.append(duplicate_result)
    duplicate_dict[search_query] = result_list


with open("data/childs_results2.json", "w", encoding="utf-8") as fp:
    json.dump(duplicate_dict , fp)

with open('glove/train.csv','w', encoding="utf-8") as file:
    for query in duplicate_dict:
            for result in duplicate_dict[query]:
                if "html_text" in result:
                    file.write(result["html_text"])
                    file.write("\n")