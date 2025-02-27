import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import simple_search_func as ss
import re


# Set global variables
PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

# panel extension
pn.extension(design="material", sizing_mode="stretch_width")

# @pn.cache # IDK what this does
# def get_data():
#     return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")

# data = get_data()

# data.tail()

# LOAD EVERYTHING
complete = pd.read_csv('../StarTrekNextGenScriptData/complete_data.csv')
complete.columns = ['index','character', 'quote', 'scene', 'location', 'view',
       'episode', 'date', 'series', 'file']
test_engine = ss.search_engine()
test_engine.bulk_load(complete[['quote']].to_dict()['quote'])

# functions
search_results = []
def search(search_engine:ss.search_engine,query:str,num_results:int=30)->list:
    global search_results
    '''Completes a search of a term on an engine'''
    results=search_engine.bw_search(query,num_results)
    search_results = search_engine.pretty_print([x[0] for x in results])
    pn.main = [search_results] # tried this
    print('success')
    return(search_engine.pretty_print([x[0] for x in results]))

def pretty_print(event):
    global search_results
    output =  '# Results\n'
    for x in search_results:
        output+='"'+re.sub(r'\s+', ' ', x[0]).strip()+'"'
        output+='\n'
        output+='**'
        output+='"'+re.sub(r'\s+', ' ', x[1]).strip()+'"'
        output+='**'
        output+='\n'
        output+='"'+re.sub(r'\s+', ' ', x[2]).strip()+'"'
        output+='\n\n'
    # output = re.sub(r'\s+', ' ', output)
    return(pn.pane.Markdown(output))



# Set Widget
text_input = pn.widgets.TextInput(name='Text Input', placeholder='candle')
search_button = pn.widgets.Button(name='Search')
# bind
search_button.on_click(lambda event: search(test_engine,text_input.value)) # lambda x

# Serve
pn.template.MaterialTemplate(
    site="SI 699 Final Project",
    title="Star Trek Search Engine",
    sidebar=[text_input,search_button],
    main=[pn.bind(pretty_print,event=search_button)],
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script

# should add character names to results