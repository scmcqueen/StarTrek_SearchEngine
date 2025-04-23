import numpy as np
import pandas as pd
import panel as pn
import re
import csv
import lightgbm as lgb
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
import os

import search_engine as se # gets the search function
import preprocess_functions as pp # gets the data preprocessing function

# set global colors
grey = '#eaeaea'
green = '#83f1b2'

# load pipeline & model
pipeline = joblib.load('data_preprocessing_pipeline.pkl') 
model = lgb.Booster(model_file='ranker_041425.txt')


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

# functions, borrowed from break_it_up.ipynb
def combine_csv_chunks(input_dir):
    """
    Recombines CSV chunks into a single CSV file.

    Args:
        input_dir (str): Directory containing CSV chunk files.
        output_file (str): Path to save the recombined CSV file.
    """
    chunk_files = sorted(
        [f for f in os.listdir(input_dir) if f.startswith("chunk_") and f.endswith(".csv")]
    )

    df_list = []
    for chunk_file in chunk_files:
        chunk_path = os.path.join(input_dir, chunk_file)
        df = pd.read_csv(chunk_path,index_col=0)
        df_list.append(df)
        print(f"Loaded: {chunk_file}")

    full_df = pd.concat(df_list, ignore_index=True)
    return(full_df)


# read in the complete data with sentiment
complete = combine_csv_chunks('sentiment_brokendown')
# drop unneeded columns
complete.drop(columns=['Unnamed: 0.1','Unnamed: 0'],inplace=True)
# fill na characters
complete['character'] = complete['character'].fillna('NA')

# read in sentence embeddings
embed_df = combine_csv_chunks('embed_brokendown')
# rename columns
embed_df.columns = [f'embedding_{x}' for x in embed_df.columns]
# get an index col for merging
embed_df=embed_df.reset_index()


# instantiate the search engine & load data
search_engine = se.search_engine(name='BM25 Engine',full_data=complete)
search_engine.bulk_load(complete[['quote']].to_dict()['quote'])

# globals
results = None
search_init = False

# functions
# search_results = []
def search(keyword:str)->pd.DataFrame:
    '''Searches the keyword returns

    Input:
        keyword: str, the term to query

    Output:
        pd.DataFrame, the ordered df of results
    '''
    # use globals
    global search_engine, embed_df, complete, pipeline, model, results, search_init
    search_init = True
    # only want to edit copies
    copy_complete = complete.copy()
    copy_embed = embed_df.copy()
    # now start search
    q_results = search_engine.bw_search(keyword,20,context=True)
    # format results
    results_df = pd.DataFrame(q_results)
    results_df.columns = ['index','bm25','prevbm25','nextbm25']
    print('We have 20 results')
    # start with merge data
    print('merging')
    merged = pp.merge_data(results_df,copy_complete,copy_embed)
    # get the feature engineering
    print('engineering')
    engineered = pp.feature_engineering(merged,copy_complete)
    # transform with columnar transform
    print('transforming')
    transformed = pipeline.transform(engineered)
    # now I can make predictions!
    print('predicting')
    preds = model.predict(transformed)
    # add predictions to data
    results_df['preds']=preds
    # rank
    results_df['rank']=results_df['preds'].rank(method='max')
    # sort
    results = results_df.sort_values('rank')
    print('finished searching')
    return results

def pretty_print(event):
    '''Displays the results of the search engine by returning a column!'''
    global results, search_init
    print('starting printing')
    opening = pn.pane.Markdown('### Results')
    column = pn.Column(opening)
    print(search_init)
    if not search_init:
        print('no data')
        return(column)
    for ind in results['index']:
        # get the pretty printed result
        pretty = search_engine.pretty_print(ind)
        column.append(pn.pane.Markdown(pretty))
    print('done printing')
    return(column)



# Set Widgets
text_input = pn.widgets.TextInput( placeholder='Try "candle"',width = 550)
search_button = pn.widgets.Button(name='Search',css_classes=['custom-button'],
    button_type='light',button_style='outline', align="center")

# bind seach to fucntion
search_button.on_click(lambda event: search(text_input.value)) # lambda x

# set title
title_text = pn.pane.Markdown('## A _Star Trek_ Search Engine that prioritizes humor', align="center")
# Serve
pn.template.MaterialTemplate(
    title="Ad Aspera per Data",
    main=pn.Column(title_text,
    pn.Row(
        text_input,
        search_button
        ),
    pn.bind(pretty_print,search_button.param.clicks))
).servable()