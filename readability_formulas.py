from readability import Readability
import nltk
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=4)
from sklearn.metrics import mean_squared_error
from scipy.stats import ttest_ind
from typing import DefaultDict, Dict, Tuple, List
from matplotlib import pyplot as plt
import plotly.express as px
from progress.bar import Bar
import os
# Import readability from readability
from readability import Readability
from collections import defaultdict
import csv
import numpy as np
import shutil

nltk.download("punkt")

readability_formulas_with_grade_levels = ['ari', 'dale_chall', 'flesch']
readability_formulas_with_grade_level = ['coleman_liau', 'flesch_kincaid', 'gunning_fog', 'linsear_write', 'spache', 'smog']
readability_formulas = readability_formulas_with_grade_levels + readability_formulas_with_grade_level

def apply_readability_formulas(text: str) -> Dict[str, Tuple[str, str]]:
    text = text.strip()
    r = Readability(text)
    if not bool(text) or r.statistics()['num_sentences'] == 0:
        return {}
    
    results = {}
    for readability_formula in readability_formulas_with_grade_levels:
        results[readability_formula] = (getattr(r, readability_formula)().score, getattr(r, readability_formula)().grade_levels[0])
    for readability_formula in readability_formulas_with_grade_level:
        if readability_formula == 'smog':
            if r.statistics()['num_sentences'] >= 30:
                results['smog'] = (r.smog(all_sentences=True).score, r.smog(all_sentences=True).grade_level)
        else:
            results[readability_formula] = (getattr(r, readability_formula)().score, getattr(r, readability_formula)().grade_level)
    return results

def readability_result_to_grade(grade: str) -> int:
    if type(grade) == int:
        return max(1, min(14, grade))
    if grade.isnumeric():
        return int(grade) if int(grade) <= 14 else 14
    if grade == "college":
        return 13
    if grade == "college_graduate":
        return 14
    return 14

def create_plot(html_text_grade_prediction: List[List[int]], description_grade_prediction: List[List[int]], search_engine: str, filename: str, rf: str):
    filename_no_ext = os.path.splitext(filename)[0]
    plot_directory = f"plots/{search_engine}/{filename_no_ext}"
    os.makedirs(f"{plot_directory}/html_text", exist_ok=True)
    os.makedirs(f"{plot_directory}/description", exist_ok=True)
    fig = px.line(x=list(range(1, 15)), y=[html_text_grade_prediction.count(i) for i in range(1, 15)], title="Grade predictions for " + rf)
    fig.write_image(f"{plot_directory}/html_text/{rf}.png")

    fig = px.line(x=list(range(1, 15)), y=[description_grade_prediction.count(i) for i in range(1, 15)], title="Grade predictions for " + rf)
    fig.write_image(f"{plot_directory}/description/{rf}.png")

def create_plots(html_text_grade_predictions: DefaultDict[str, List[int]], description_grade_predictions: DefaultDict[str, List[int]], search_engine: str, filename: str):
    for rf in readability_formulas:
        html_text_grade_prediction = html_text_grade_predictions[rf]
        description_grade_prediction = description_grade_predictions[rf]
        create_plot(html_text_grade_prediction, description_grade_prediction, search_engine, filename, rf)

def perform_ttest(html_text_grade_prediction: List[int], description_grade_prediction: List[int]):
    return ttest_ind(html_text_grade_prediction, description_grade_prediction, nan_policy='omit', alternative='two-sided', equal_var=False)

def perform_ttests(grade_predictions1: DefaultDict[str, List[int]], grade_predictions2: DefaultDict[str, List[int]], search_engine: str, filename: str):
    ttests: Dict[str, int] = {}
    for rf in readability_formulas:
        if rf == 'smog':
            continue
        grade_prediction1 = grade_predictions1[rf]
        grade_prediction2 = grade_predictions2[rf]
        ttests[rf] = perform_ttest(grade_prediction1, grade_prediction2)
    os.makedirs(f"ttests/{search_engine}", exist_ok=True)
    with open(f"ttests/{search_engine}/{os.path.splitext(filename)[0]}.csv", 'w', newline='') as f:
        header = ['rf', 't-statistic', 'p-value']
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for key, value in ttests.items():
            writer.writerow({'rf': key, 't-statistic': value.statistic, 'p-value': value.pvalue})

def save_readability_results(html_text_grade_predictions: DefaultDict[str, List[int]], description_grade_predictions: DefaultDict[str, List[int]], search_engine: str, filename: str):
    os.makedirs(f"readability_results/{search_engine}", exist_ok=True)
    with open(f"readability_results/{search_engine}/{os.path.splitext(filename)[0]}.csv", 'w', newline='') as f:
        import csv
        header = ['rf', 'html_text', 'description']
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for rf in readability_formulas:
            writer.writerow({'rf': rf, 'html_text': html_text_grade_predictions[rf], 'description': description_grade_predictions[rf]})

def load_readability_results():
    for search_engine in ['google', 'bing']:
        adult_grade_predictions: Dict[str, Tuple[List[int], List[int]]] = {}
        child_grade_predictions: Dict[str, Tuple[List[int], List[int]]] = {}
        for filename in os.listdir(f"readability_results/{search_engine}"):
            with open(f"readability_results/{search_engine}/{filename}") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "adult" in filename:
                        adult_grade_predictions[row['rf']] = ((np.fromstring(row['html_text'].strip('[]'), sep=',').tolist()), np.fromstring(row['description'].strip('[]'), sep=',').tolist())
                    else:
                        child_grade_predictions[row['rf']] = (np.fromstring(row['html_text'].strip('[]'), sep=',').tolist(), np.fromstring(row['description'].strip('[]'), sep=',').tolist())
        adult_html_text_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
        adult_description_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
        child_html_text_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
        child_description_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
        
        for rf in readability_formulas:
            adult_html_text_grade_predictions[rf] = adult_grade_predictions[rf][0]
            adult_description_grade_predictions[rf] = adult_grade_predictions[rf][1]
            child_html_text_grade_predictions[rf] = child_grade_predictions[rf][0]
            child_description_grade_predictions[rf] = child_grade_predictions[rf][1]
        
        perform_ttests(child_html_text_grade_predictions, adult_html_text_grade_predictions, search_engine, "child-adult-html")
        perform_ttests(child_description_grade_predictions, adult_description_grade_predictions, search_engine, "child-adult-description")

if __name__ == "__main__":
    for filename in os.listdir("data"):
        queries = pd.read_json(f"data/{filename}")
        print(f"Processing {filename}...")
        for search_engine in ['google', 'bing']:
            with Bar(f'Calculating readability metrics for {search_engine.capitalize()}', max=len(list(queries.items()))) as bar:
                html_text_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
                description_grade_predictions: DefaultDict[str, List[int]] = defaultdict(list)
                for _, query in queries.items():
                    result_page = query[search_engine]
                    for result in result_page:
                        readability_html_text = {}
                        readability_description = {}
                        if 'html_text' in result:
                            readability_html_text = apply_readability_formulas(result['html_text'])
                        if 'description' in result:
                            readability_description = apply_readability_formulas(result['description'])
                        for rf in readability_formulas:
                                if rf in readability_html_text:
                                    html_text_grade_predictions[rf].append(readability_result_to_grade(readability_html_text[rf][1]))
                                else:
                                    html_text_grade_predictions[rf].append(float('NaN'))
                                if rf in readability_description:
                                    description_grade_predictions[rf].append(readability_result_to_grade(readability_description[rf][1]))
                                else:
                                    description_grade_predictions[rf].append(float('NaN'))
                    bar.next()
            create_plots(html_text_grade_predictions, description_grade_predictions, search_engine, filename)
            perform_ttests(html_text_grade_predictions, description_grade_predictions, search_engine, filename)
            save_readability_results(html_text_grade_predictions, description_grade_predictions, search_engine, filename)
    
    load_readability_results()
    shutil.rmtree("readability_results")
