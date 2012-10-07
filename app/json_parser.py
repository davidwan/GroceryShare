import nltk
from urllib import urlopen
import json
from collections import defaultdict


def get_recipe(query):
    # Extract pure text from webpage. 

    url = "http://www.recipepuppy.com/api/?q=" + str(query)
    html = urlopen(url).read()  
    raw = nltk.clean_html(html)  
    # Parse through JSON text and store information in dictionaries/lists
    r = json.loads(raw)
    d = defaultdict(lambda : defaultdict(str))

    for i in range(len(r['results'])):
      inner = r['results'][i]
      d[i]['title'] = str(inner['title'])  
      d[i]['link'] = str(inner['href'])
      d[i]['ingredients'] = str(inner['ingredients']).split(",")
    
    return d