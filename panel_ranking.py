import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import simple_search_func as ss
import re
import csv

# GUYS I DON"T NEED THIS FILE

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

# globals
ranking = []
display = []
results = None
craines = pn.widgets.Button(name='Craines')

# functions
search_results = []
def search(search_engine:ss.search_engine,query:str,num_results:int=30)->list:
    global search_results, results
    '''Completes a search of a term on an engine'''
    results=search_engine.bw_search(query,num_results)
    search_results = search_engine.pretty_print([x[0] for x in results])
    #pn.main = [search_results] # tried this
    print('success')
    return(search_engine.pretty_print([x[0] for x in results]))


def pretty_print(event):
    global search_results, ranking, craines, display
    temp_open = pn.pane.Markdown('# Ranking\n')
    main = pn.Row()
    column = pn.Column(temp_open)
    display = []
    ranking = []
    output='# Results\n'
    
    #get results
    for x in search_results:
        output+='"'+re.sub(r'\s+', ' ', x[0]).strip()+'"'
        output+='\n'
        output+='**'
        output+='"'+re.sub(r'\s+', ' ', x[1]).strip()+'"'
        output+='**'
        output+='\n'
        output+='"'+re.sub(r'\s+', ' ', x[2]).strip()+'"'
        output+='\n'
        output+='\n'

    main.append(pn.pane.Markdown(output)) # pretty print all results
    if search_results==[]:
        return(main)
    for i in range(1,11):
        #drop_down = pn.widgets.Select(name=f'Select {i}', options=search_results)
        drop_down = pn.widgets.Select(name=f'Select {i}', options=[x[1] for x in search_results],size=10)
        ranking.append(drop_down)
        column.append(drop_down)

    column.append(craines)
    main.append(column)
    return(main)

def save_ranking(ranking:list): #add documentation
    length = len(ranking)
    ranking_output  = {}
    for x in range(length):
        ranking_output[x+1]=ranking[x].value
    with open(f"Evaluation/rankings_{text_input.value}_{name_input.value}.csv", "w", newline="") as f:
        # I need to update this
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

craines.on_click(lambda event: save_ranking(ranking))

# Serve
pn.template.MaterialTemplate(
    site="SI 699 Final Project",
    title="Star Trek Search Engine Ranking Page",
    sidebar=[text_input,name_input,search_button],
    main=[pn.bind(pretty_print,event=search_button)],
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script

# should add character names to results