This project contains multiple files used to retrieve, clean and apply readability formulaes.

Scrape SERPs by using bee.py and the bing.py files.

Afterwards use soup.py to get the content of the links retrieved in the previous file, to collect and clean the HTML retrieved.

Lastly use readability_formulas.py to collect readability data.

To use readnet first train a model using the readnet.py file, and afterwards load the model. A flag can be set in the code wheter you want to write or read.

readnet_analysis.py applies readnet to match the readnet score with a grade.