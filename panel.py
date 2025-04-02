import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import simple_search_func as ss
import re
import csv

pn.extension( global_css=[''':root { --design-primary-color: black;
    --mdc-theme-background: #eaeaea; /* Green background */}
    body {
    --mdc-theme-background: #eaeaea; /* Green background */
}
'''])

pn.extension(raw_css=['''.custom-button {
        background-color: #c1ff72;
        color: white;
        primary-color: red;
        border-radius: 5px;
        border-width: 0px;
    }
    '''])



# LOAD EVERYTHING
complete = pd.read_csv('https://scmcqueen.github.io/StarTrekScriptData/complete_data.csv')
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
text_input = pn.widgets.TextInput( placeholder='Try "candle"',width = 900)
search_button = pn.widgets.Button(name='Search',css_classes=['custom-button'],
    button_type='light',button_style='outline', align="center")
# bind
search_button.on_click(lambda event: search(test_engine,text_input.value)) # lambda x

title_text = pn.pane.Markdown('## A _Star Trek_ Search Engine', align="center")

# Serve
pn.template.MaterialTemplate(
    title="Ad Aspera per Data",
    # sidebar=['hello'],
    main=pn.Column(title_text,
    pn.Row(pn.Spacer(sizing_mode="stretch_width"),
        text_input,
        search_button,
        pn.Spacer(sizing_mode="stretch_width")),
    pn.bind(pretty_print,event=search_button)),
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script

# should add character names to results