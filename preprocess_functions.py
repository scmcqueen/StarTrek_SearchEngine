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

def feature_engineering(full_data:pd.DataFrame,complete:pd.DataFrame)->pd.DataFrame:
    '''Add more features to the df.

    Input:
        full_data: pd.DataFrame
        complete: pd.DataFrame

    Output:
        pd.DataFrame,
    '''
    # get the length of each quote
    full_data['quote_len']=full_data['quote'].apply(lambda z: len(z.split()))

    # get the total quotes per character across ALL series (Worf & O'Brien)
    quote_count = complete.groupby('character').count()['quote']
    full_data['total_quotes_char']=full_data['character'].apply(lambda x: quote_count[x])

    # get the character overall quotes in episode
    ep_quote = complete.groupby(['character','file']).count()['quote']
    full_data['episode_quotes']=full_data.apply(lambda x: ep_quote[x['character'],x['file']],axis=1)

    # get previous quote info
    complete['prev_character']=complete['character'].shift(1)
    complete['prev_sent']=complete['sentiment'].shift(1)
    complete['prev_quote_len']=complete['quote'].apply(lambda z: len(str(z).split())).shift(1)
    full_data = full_data.merge(complete[['prev_character','prev_quote_len','prev_sent','index']],on='index',how='left')

    # get next quote info
    complete['next_character']=complete['character'].shift(-1)
    complete['next_sent']=complete['sentiment'].shift(-1)
    complete['next_quote_len']=complete['quote'].apply(lambda z: len(str(z).split())).shift(-1)
    full_data = full_data.merge(complete[['next_character','next_quote_len','next_sent','index']],on='index',how='left')
    return(full_data)

def merge_data(bm25_df:pd.DataFrame,complete_df:pd.DataFrame,embed_df:pd.DataFrame):
    '''
    Merges all of the data needed into one nice frame!

    Input:
        bm25_df: pd.DataFrame, search results from simple bm25
        embed_df: pd.DataFrame, embedding data
        complete_df: pd.DataFrame, full context

    Output:
        pd.DataFrame, combined with all the data
    '''
    full_bm = bm25_df.merge(complete_df,on=['index'],how='left')
    full_em = full_bm.merge(embed_df,on=['index'],how='left')
    return(full_em)
