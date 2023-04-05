import json
import requests
from bs4 import BeautifulSoup
import re

f = open("adult_queries/non_cleaned_html.json" , "rb" )
queries = json.load(f)
f.close()

## i have no idea about this, but i fiddled around with it for a while and this was what ended up working.
def remove_tags(html):
 
    soup = BeautifulSoup(html, "html.parser")

    # Remove CSS, style, script tags and their contents
    for tag in soup(["script", "style", "link", "head", "nav"]):
        tag.extract()
    # Get the text
    p_tags = soup.find_all('p')
    text = ""
    
    for p_tag in p_tags:
        for a_tag in p_tag.find_all('a'):
            a_tag.extract()
        for link_tag in p_tag.find_all('link'):
            link_tag.extract()
        for content in p_tag.contents:
            if hasattr(content, "text"):
                text += content.text + " "
            else:
                text += content + " "
            ## if <span> extract text put it in.
            ## if a_tag extract text and put it in.
            ## add the text and then boom boom.


    result = re.sub(r'\[.*?\]', '', text)
    result = re.sub(r'^', '', result)
    result = re.sub(r'\\"', '', result)
    result = re.sub(r'|"', '', result)
    result = re.sub(r'\\""', '', result)
    # removes any amount of spaces and replaces them with 1 space. Thx chatgpt.
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\n', '', result)
    
    return result

def clean_description(desc):
    words = desc.split()
    # Keep only words with English characters
    html = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]
    # Join the English words back into a string
    joined_description = ' '.join(html)
    return joined_description


def getResults(queries):
    duplicate_dict = queries
    for key, query in queries.items():
        for description_key in ["bing_results", "results"]: 
            result_list = []
            for result in query[description_key]:
                duplicate_result = result
                try:
                    url = result["url"]
                    response = requests.get(url, timeout=5)
                    if response.status_code > 299:
                        duplicate_result["html_text"] = ""
                        result_list.append(duplicate_result)
                        break
                    content_as_string = response.content.decode('utf-8')
                    duplicate_result["html_text"] = content_as_string
                except:
                    print("error occured")
                    duplicate_result["html_text"] = ""
                result_list.append(duplicate_result)
            duplicate_dict[key] = queries[key]
            duplicate_dict[key][description_key] = result_list
    return duplicate_dict

def clean_up_descriptions(queries):
    duplicate_dict = queries
    for key, query in queries.items():
        for description_key in ["bing_results", "results"]:
            result_list = []
            for result in query[description_key]:
                duplicate_result = result
                description = clean_description(result["description"])
                duplicate_result["description"] = description
                result_list.append(duplicate_result)
            duplicate_dict[key][description_key] = result_list
    return duplicate_dict

def clean_up_html(queries):
    duplicate_dict = queries
    for key, query in queries.items():
        for description_key in ["bing_results", "results"]:
            result_list = []
            for result in query[description_key]:
                duplicate_result = result
                cleaned_html = ""
                if "html_text" in result:
                    cleaned_html = remove_tags(result["html_text"])
                duplicate_result["html_text"] = cleaned_html
                result_list.append(duplicate_result)
            duplicate_dict[key][description_key] = result_list
    return duplicate_dict

# results = getResults(queries)
results = clean_up_html(queries)
with open("adult_queries/cleaned_htnl.json", "w", encoding="utf-8") as fp:
    json.dump(results , fp, ensure_ascii=False)