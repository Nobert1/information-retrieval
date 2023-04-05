from readability import Readability
import nltk
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=4)
from sklearn.metrics import mean_squared_error

nltk.download("punkt")

readability_formulas_with_grade_levels = ['ari', 'dale_chall', 'flesch']
readability_formulas_with_grade_level = ['coleman_liau', 'flesch_kincaid', 'gunning_fog', 'linsear_write', 'spache', 'smog']
readability_formulas = readability_formulas_with_grade_levels + readability_formulas_with_grade_level

def apply_readability_formulas(text: str) -> dict[str, tuple[str, str]]:
    r = Readability(text)
    
    if not bool(text) or r.statistics()['num_words'] < 100:
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
    if grade == "college_graduate":
        return 14
    if grade == "college":
        return 13
    return int(grade)


if __name__ == "__main__":
    queries = pd.read_json("kids_queries/cleaned_html_results.json")
    query_result_readability_formula_mse = pd.DataFrame()
    for _, query in queries.items():
        for search_engine_result_page in ['results', 'bing_results']:
            grade_pred: dict[str, list[int]] = {}
            for readability_formula in readability_formulas:
                grade_pred[readability_formula] = []
            for result in query[search_engine_result_page]:
                if 'html_text' in result:
                    readability_results = apply_readability_formulas(result['html_text'])
                    for readability_formula in readability_formulas:
                        if readability_formula in readability_results:
                             grade_pred[readability_formula].append(readability_result_to_grade(readability_results[readability_formula][1]))
                        else:
                            grade_pred[readability_formula].append(0)
            for readability_formula in readability_formulas:<
                if len(grade_pred[readability_formula]) == 0:
                    continue
                grade_true = [readability_result_to_grade(query['Grade'])] * len(grade_pred[readability_formula])
                mse = mean_squared_error(grade_true, grade_pred[readability_formula]) 
                query_result_readability_formula_mse.loc[readability_formula, query['queries']] = mse
    print(query_result_readability_formula_mse)