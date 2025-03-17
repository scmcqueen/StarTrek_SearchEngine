import pandas as pd
from path import Path
import os
from collections import defaultdict
from math import log
import string
from collections import Counter

# functions
def normalize_string(input_string: str) -> str:
    translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = ' '.join(string_without_punc.split())
    return string_without_double_spaces.lower()

def update_url_scores(old: dict[str, float], new: dict[str, float]):
    for url, score in new.items():
        if url in old:
            old[url] += score
        else:
            old[url] = score
    return old

class search_engine:
    '''Search engine class'''
    def __init__(self, index:dict[str, dict[str, int]]=None, docs: dict[str, str]=None,original_docs: dict[str, str]=None,k1:float=1.5,b:float=0.75,name:str='Default Search Engine'):
        '''Instantiate the search engine class.
        Input:
            index: dict[str, dict[int,int]], the inverted index
            docs: dict[int, str], key is the id of the quote and value is the quote text
            k1: float, k1 constant to use for bm25
            b: float, b constant to use for bm25
        Output:
            None, class instantiation
        '''
        if index is None:
            self.index = defaultdict(lambda: defaultdict(int))
        else:
            self.index = index
        if docs is None:
            self.docs = {}
        else:
            self.docs = docs
        if original_docs is None:
            self.original_docs = {}
        else:
            self.original_docs = original_docs
        self.k1 =k1
        self.b = b
        self.name = name
        self.full_data = None

    def __str__(self)->str:
        '''Print readable name of the search engine
        Output:
            str: name of the instance
        '''
        return(self.name)

    def bulk_load(self,data:dict)->None:
        '''Bulk loads new documents to add to the search engine.

        Input:
            data: dict[int,str], where int is the id and str is the content
        '''
        original_len = len(self.docs.keys())
        for ind in data.keys():
            # get the content & the id
            content = data[ind]
            id = ind
            # add original docs
            self.original_docs[id]=content
            # add to doc list
            self.docs[id]=normalize_string(content)
            # normalize content
            words = normalize_string(content).split(" ")
            # update the index
            for word in words:
                self.index[word][id] += 1
        new_len =original_len = len(self.docs.keys())
        print(f'We have added {new_len-original_len} documents. The engine now has {new_len} documents.')

    def add_df(self,dataframe:pd.DataFrame)->None:
        ''' Adds a data frame with the same indices to reference more information.

        Input:
            dataframe: pd.Dataframe, same indices
        '''
        self.full_data = dataframe
        print('Complete data added.')
        return

    def load(self,document:str)->None:
        '''Load a single document into the search engine. Ideally this should not be used.

        Input:
            document: str, the new text document to add to the search engine.
        '''
        new_id = len(self.docs.keys())
        self.docs[new_id]=normalize_string(document)
        words = normalize_string(document).split(" ")
        for word in words:
            self.index[word][new_id]

    def num_docs(self)->int:
        '''Returns the number of docs

        Output:
            int: length of docs
        '''
        return len(self.docs.keys())

    def find_ids(self,keyword:string)->dict:
        keyword =normalize_string(keyword)
        return self.index[keyword]

    def bw_idf(self,keyword:str)->float:
    # for each term, get the idf
        num_docs = self.num_docs()
        n_kw = len(self.find_ids(keyword))
        return log((num_docs-n_kw+0.5)/(n_kw+0.5)+1)
    
    def bm25(self, keyword:str)-> dict[str, float]:
        result = {}
        idf = self.bw_idf(keyword)
        avg_ql = sum(len(d) for d in self.docs.values()) / len(self.docs)
        for id, freq in self.find_ids(keyword).items():
            num = freq * (self.k1+1)
            denom = freq+self.k1*(1 - self.b + self.b * len(self.docs[id]) / avg_ql)
            result[id]=idf * num /denom
        return result
    
    def bw_search(self,query:str,limit:int=None)->dict[str,float]:
        kws = normalize_string(query).split(" ")
        scores ={} # dict[str, float] 
        for k in kws:
            kw_url_score = self.bm25(k)
            scores = update_url_scores(scores,kw_url_score)
        sort_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]),reverse=True)
        if limit is not None:
            sort_scores = sort_scores[:limit]
        return sort_scores
    
    def pretty_print(self,ids:list)->list:
        '''Prints the quotes instead of a list of ids'''
        # get context
        output = []
        for x in ids:
            context = [self.original_docs[x-1],self.original_docs[x],self.original_docs[x+1]]
            output.append(context)
        return(output)