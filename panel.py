import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import re
import csv
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from spacy.tokens import Doc
import csv
import altair as alt
import joblib

import search_engine as se # gets the search function
import preprocess_functions as pp # gets the data preprocessing function

# set global colors
grey = '#eaeaea'
green = '#83f1b2'


pn.extension( global_css=[''':root { --design-primary-color: black;
    --mdc-theme-background: XXX; /* Grey background */}
    body {
    --mdc-theme-background: XXX; /* Grey background */
}
'''.replace('XXX',grey)])

pn.extension(raw_css=['''.custom-button {
        background-color: YYY;
        color: white;
        border-radius: 5px;
        border-width: 0px;
    }
    '''.replace('YYY',green)])



# LOAD EVERYTHING
complete = pd.read_csv('https://scmcqueen.github.io/StarTrekScriptData/complete_data.csv')
complete.columns = ['index','character', 'quote', 'scene', 'location', 'view',
       'episode', 'date', 'series', 'file']
# test_engine = ss.search_engine()
# test_engine.bulk_load(complete[['quote']].to_dict()['quote'])
# test_engine.add_df(complete)

# globals
ranking = []
results = None
craines = pn.widgets.Button(name='Craines')

# functions
# search_results = []
# def search(search_engine:ss.search_engine,query:str,num_results:int=30)->list:
#     global search_results, results
#     '''Completes a search of a term on an engine'''
#     results=search_engine.bw_search(query,num_results)
#     search_results = search_engine.pretty_print([x[0] for x in results])
#     pn.main = [search_results] # tried this
#     print('success')
#     return(search_engine.pretty_print([x[0] for x in results]))

def pretty_print(event):
    global search_results, ranking, craines
    temp_open = pn.pane.Markdown('### Results')
    column = pn.Column(temp_open)
    # output =  ''
    # counter = 0
    # ranking = []
    # for x in search_results:
    #     output+='"'+re.sub(r'\s+', ' ', x[0]).strip()+'"'
    #     output+='\n'
    #     output+='**'
    #     output+=x[1]
    #     # output+='"'+re.sub(r'\s+', ' ', x[1]).strip()+'"'
    #     output+='**'
    #     output+='\n'
    #     output+='"'+re.sub(r'\s+', ' ', x[2]).strip()+'"'
    #     column.append(pn.pane.Markdown(output))
    #     output=''
    #     # temp = pn.widgets.TextInput(name=f'Ranking {str(counter)}', placeholder='candle')
    #     radio = pn.widgets.RadioButtonGroup(name=f'Ranking {str(counter)}', 
    #                                         options=['Relevant','No'], button_type='success')
    #     ranking.append(radio)
    #     column.append(radio)
    #     counter +=1
    # # TEMPORARILY COMMENT EVERYTHING OUT
    column.append(pn.pane.Markdown('''
        RIKER: I don't like fudge.
        **TROI: Really. I never met a chocolate I didn't like.**
        RIKER: Doesn't it taste good?

        _Star Trek: The Next Generation_, “The Game”
    '''))
    column.append(pn.pane.Markdown('''
        RIKER: Sure. I'll catch up with you later.
        **RIKER: Chocolate ice cream. Chocolate fudge. Chocolate chips. You're not depressed, are you?**
        TROI: I'm fine, Commander.

        _Star Trek: The Next Generation_, “The Game”
    '''))

    column.append(pn.pane.Markdown('''
        RIKER: I never knew it was a ritual. 
        **TROI: Chocolate is a serious thing.**
        RIKER: You know... I brought something back from Risa. It's better than chocolate.

        _Star Trek: The Next Generation_, “The Game”
    '''))
    column.append(pn.pane.Markdown('''
        WORF: I believe Commander Data's painting is making me dizzy... 
        **WORF: I thought this cake was chocolate... **
        TROI: Don't I wish.

        _Star Trek: The Next Generation_, “Parallels”
    '''))
    column.append(pn.pane.Markdown('''
        TROI: Transfer my mother's letters to my viewer...
        **TROI : ... and computer, I'd like a... a real chocolate sundae.**
        COMPUTER: Define ""real"" in context, please.

        _Star Trek: The Next Generation_, “The Price”
    '''))
    column.append(pn.pane.Markdown('''
        DATA: When Counselor Troi is in an unhappy mood, she often has something chocolate... 
        **Q: Chocolate...**
        DATA: For example, a hot fudge sundae. I cannot speak from personal experience, but I have seen it often has a profound psychological impact.
        
        _Star Trek: The Next Generation_, “Deja Q”
    '''))
    return(column)



# Set Widget
text_input = pn.widgets.TextInput( placeholder='Try "candle"',width = 550)
search_button = pn.widgets.Button(name='Search',css_classes=['custom-button'],
    button_type='light',button_style='outline', align="center")
# bind
search_button.on_click(lambda event: search(test_engine,text_input.value)) # lambda x

title_text = pn.pane.Markdown('## A _Star Trek_ Search Engine that prioritizes humor', align="center")

# Serve
pn.template.MaterialTemplate(
    title="Ad Aspera per Data",
    main=pn.Column(title_text,
    pn.Row(#pn.Spacer(sizing_mode="stretch_width"),
        text_input,
        search_button,
        #pn.Spacer(sizing_mode="stretch_width")
        ),
    pn.bind(pretty_print,event=search_button)),
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script

# should add character names to results