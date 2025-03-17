import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import simple_search_func as ss
import re
import csv

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
test_engine.add_df(complete)

# globals
ranking = []
results = None
craines = pn.widgets.Button(name='Craines')

# functions
search_results = []
def search(search_engine:ss.search_engine,query:str,num_results:int=30)->list:
    global search_results, results
    '''Completes a search of a term on an engine'''
    results=search_engine.bw_search(query,num_results)
    search_results = search_engine.pretty_print([x[0] for x in results])
    pn.main = [search_results] # tried this
    print('success')
    return(search_engine.pretty_print([x[0] for x in results]))

def pretty_print(event):
    global search_results, ranking, craines
    temp_open = pn.pane.Markdown('# Results\n')
    column = pn.Column(temp_open)
    output =  ''
    counter = 0
    ranking = []
    for x in search_results:
        output+='"'+re.sub(r'\s+', ' ', x[0]).strip()+'"'
        output+='\n'
        output+='**'
        output+='"'+re.sub(r'\s+', ' ', x[1]).strip()+'"'
        output+='**'
        output+='\n'
        output+='"'+re.sub(r'\s+', ' ', x[2]).strip()+'"'
        column.append(pn.pane.Markdown(output))
        output=''
        # temp = pn.widgets.TextInput(name=f'Ranking {str(counter)}', placeholder='candle')
        radio = pn.widgets.RadioButtonGroup(name=f'Ranking {str(counter)}', 
                                            options=['Relevant','No'], button_type='success')
        ranking.append(radio)
        column.append(radio)
        counter +=1
    # output = re.sub(r'\s+', ' ', output)
    column.append(craines)
    return(column)

def save_ranking(search_results:str):
    length = len(search_results)
    ranking_output  = {}
    for x in range(length):
        #ranking_output[search_results[x][1]]=ranking[x].value
        ranking_output[results[x][0]]=ranking[x].value
    with open(f"Evaluation/rankings_{text_input.value}_{name_input.value}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, ranking_output.keys())
        w.writeheader()
        w.writerow(ranking_output)
    print('success save')
    return None


# Set Widget
text_input = pn.widgets.TextInput(name='Search Term', placeholder='candle')
name_input = pn.widgets.TextInput(name='Username', placeholder='Skyeler')
search_button = pn.widgets.Button(name='Search')
# bind
search_button.on_click(lambda event: search(test_engine,text_input.value)) # lambda x
craines.on_click(lambda event: save_ranking(search_results))

# Serve
pn.template.MaterialTemplate(
    site="SI 699 Final Project",
    title="Star Trek Search Engine",
    sidebar=[text_input,search_button,name_input],
    main=[pn.bind(pretty_print,event=search_button)],
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script

# should add character names to results