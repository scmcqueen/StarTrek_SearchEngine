# Imports
import pandas as pd
from path import Path
import os
from collections import defaultdict
from math import log
import string
from collections import Counter
import re

def update_url_scores(old: dict[str, float], new: dict[str, float]):
    '''This function adds two dictionaries together'''
    for url, score in new.items():
        if url in old:
            old[url] += score
        else:
            old[url] = score
    return old


def normalize_string(input_string: str) -> str:
    '''This function processes a string by removing punctuation,
    making text lowercase, and getting rid of extra spaces

    For example:
        "Hello,  HI!!! How are     you?"
    becomes
        "hello hi how are you"
    '''
    translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = ' '.join(string_without_punc.split())
    return string_without_double_spaces.lower()

class search_engine:
    '''This class creates a search engine object'''
    def __init__(self, index:dict[str, dict[str, int]]=None, docs: dict[str, str]=None,
        original_docs: dict[str, str]=None,k1:float=1.5,b:float=0.75,
        name:str='Default Search Engine',full_data: pd.DataFrame=None):
        '''
        Instantiate an instance of the search engine class.

        Input:
            index: dict[str, dict[int,int]], the inverted index
            docs: dict[int, str], key is the id of the quote and value is the quote text
            original_docs:
            k1: float, k1 constant to use for bm25
            b: float, b constant to use for bm25
            name: string, name used for the search engine instance
            full_data:  pd.DataFrame, the original dataset used

        Output:
            search engine!
        '''
        # set index
        if index is None: self.index = defaultdict(lambda: defaultdict(int))
        else: self.index = index
        # set docs
        if docs is None: self.docs = {}
        else: self.docs = docs
        # set original docs
        if original_docs is None: self.original_docs = {}
        else: self.original_docs = original_docs
        # set k1
        self.k1 = k1
        # set b
        self.b = b
        # set name
        self.name = name
        # set full_data
        self.full_data = full_data

    def __str__(self)->str:
        '''
        Prints a readable name of the search engine

        Output:
            str: name of the instance
        '''
        return(self.name)

    def bulk_load(self,data:dict,full_data:pd.DataFrame=None)->None:
        '''
        Bulk loads new documents to the search engine.

        Input:
            data: dict, the formatted data
            full_data: pd.DataFrame, the data with the full info
        '''
        # get the original size of the docs
        original_len = len(self.docs.keys())
        # for each index in the data
        for ind in data.keys():
            content = data[ind] # quote text
            # add to original docs
            self.original_docs[ind]=content
            # normalize content & add to docs
            n_content = normalize_string(str(content))
            self.docs[ind]=n_content

            # now we want to created the inverted index based on words
            words = n_content.split(" ")
            for w in words:
                self.index[w][ind]+=1 # update count of word per index
        # get new length
        new_len = len(self.docs.keys())
        print(f'We added {new_len-original_len} documents. The engine now has {new_len} documents.')

    def individual_load(self, document:str)-> None:
        '''
        Load a single document into the search engine. Ideally this should not be used.

        Input:
            document: str, the new text document to add to the search engine.
        '''
        # assign new id
        new_id = len(self.docs.keys())
        # add to docs & original docs
        self.original_docs[new_id]=document
        n_docs = normalize_string(document)
        self.docs[new_id]=n_docs
        # now we need to update the inverted index
        words = n_docs.split(" ")
        for w in words:
            self.index[w][new_id]
        print(f'Added document "{document}" to search engine.')

    def num_docs(self)->int:
        '''
        Returns the number of docs

        Output:
            int: length of docs
        '''
        return len(self.docs.keys())

    def find_ids(self, keyword:str)->dict:
        '''
        Find the doc ids that contain a keyword.

        Input:
            keyword: str, the word to search
        Returns:
            dict: keys are the indices and the values are
                the frequency of the word in the document
        '''
        key = normalize_string(keyword)
        return(self.index[key])

    def bw_idf(self,keyword:str)-> float:
        '''
        Find the inverse document frequency for a term

        Input:
            keyword: str, word to search

        Output:
            float: the idf score
        '''
        num_docs = self.num_docs()
        keyword = normalize_string(keyword)
        n_kw = len(self.find_ids(keyword))
        idf = log((num_docs-n_kw+0.5)/(n_kw+0.5)+1)
        return(idf)

    def bm25(self,keyword:str)-> dict[str, float]:
        '''
        Calculate the bm25 score for every document

        Input:
            keyword: str, word to search

        Output:
            dict[str, float]: dict of doc ids & the bm25 score
        '''
        result = {} # instantiate the output
        keyword = normalize_string(keyword)
        idf = self.bw_idf(keyword) # get the idf score
        # get the avg len of a document
        avg_ql = sum(len(d) for d in self.docs.values()) / len(self.docs)
        # calculate the bw score for each
        for id, freq in self.find_ids(keyword).items(): # for doc id & word freq
            numerator = freq*(self.k1+1)
            denominator = freq+self.k1*(1 - self.b + self.b * len(self.docs[id]) / avg_ql)
            result[id]=idf*numerator / denominator
        # return dict with the ids & scores
        return result

    def bw_search(self,query:str,limit:int=None,context:bool=False)->dict[str,float]:
        '''
        Completes the bm25 search of the documents using the query and returns

        Input:
            query: str, the query to search through the documents
            limit: int, limits the number of documents
            context: bool, if true return also the bm-scores of the lines before & after the selected lines.
                There must exist a limit for this to be true.

        Output:
            dict[str,float]: the index and the bm25 score
        '''
        # split the query & normalize it
        kws = normalize_string(query).split(" ")
        scores = {} # initialize output
        for k in kws:
            kw_score = self.bm25(k) # get the scores for this word
            scores = update_url_scores(scores,kw_score) # add the dict values together
        # sort the scores by the bm25 score
        sorted_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]),reverse=True)
        output = sorted_scores.copy()
        # limit the score output
        if limit is not None:
            output = sorted_scores[:limit]
            # check if we need to get context
            if context:
                # get index, score, score of line before, score of line after
                output = [[x[0],x[1], scores[x[0]-1] if x[0]-1 in scores.keys() else 0, scores[x[0]+1] if x[0]+1 in scores.keys() else 0 ] for x in output]

        return(output)

    def pretty_print(self, index:int)->str:
        '''
        Prints the speaker, line, and context for a specific query.

        Input:
            index: int, the index in the data full data frame.

        Output:
            string: a well formatted string
        '''
        # maybe could do this more efficiently
        q = self.full_data.iloc[index]['quote'] # get quote
        char = self.full_data.iloc[index]['character'] # get character (& make lowercase)
        ep = self.full_data.iloc[index]['episode'] # get episode
        series = self.full_data.iloc[index]['series'] # get series
        date = self.full_data.iloc[index]['date'] # get date
        # previous values
        p_q = self.full_data.iloc[index-1]['quote'] # get previous quote
        p_char = self.full_data.iloc[index-1]['character'] # get previous character (& make lowercase)
        # next values
        n_q = self.full_data.iloc[index+1]['quote'] # get next quote
        n_char = self.full_data.iloc[index+1]['character'] # get next character (& make lowercase)

        output = f'{p_char}: {p_q} \n {char}: {q} \n {n_char}: {n_q} \n \n "{ep}", __Star Trek: {series}__, {date}'
        return(output)

    def old_pretty_print(self,ids:list)->list:
        '''Prints the quotes instead of a list of ids'''
        # get context
        output = []
        for x in ids:
            context = [self.full_data['character'].iloc[x-1]+': '+self.original_docs[x-1],
                       self.full_data['character'].iloc[x]+': '+self.original_docs[x],
                       self.full_data['character'].iloc[x+1]+': '+self.original_docs[x+1]]
            output.append(context)
        return(output)