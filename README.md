# Ad Aspera Per Data ✨
## A Star Trek Search Engine
Welcome to "Ad Aspera Per Data" an independent study into search engines and ML Ops. Started as a project for my SI 699: Big Data Mastery Course at the University of Michigan.

You can run this application locally, or check out my [Hugging Face](https://huggingface.co/spaces/sklearnsorenqueen/startreksearchengine) page.

### How to Run Application Locally 👩🏼‍💻
1. Download the code or clone this repo
2. Open up a terminal (cd to where the code is saved)
3. Run "panel serve panel.py "
4. Click 'allow' if you get a pop-up
5. Navigate to [http://localhost:5006/panel](http://localhost:5006/panel) in your browser

### Contents 📚

#### Code Overview
* break_it_up.ipynb: this file has the code to break down large files into smaller chunks.
* panel.py: this file contains the code with the panel web app.
* preprocess_functions.py: this file has the code for the functions that engineer the data features needed to run the model.
* qsf_filler.ipynb: this notebook has the data needed to create the qualtrics qsf files and then read the results.
* Search_Engine.ipynb: the notebook I used to develop the search engine class
* search_engine.py: the file with the search engine class data
* sent_emb.ipynb: this notebook gets the sentence embeddings & sentiment for the quotes. It generates the st_embeddings.csv file, which is too big to be stored on Github.
* Training_ML_Model.ipynb: this file is used to train the LambdaRank model.
* visualizations.ipynb: the notebook used to generate my visualizations!

#### Files Overview
* complete_sentiment.csv: this file has the complete _Star Trek_ quote data including the sentiment!
* data_preprocessing_pipieline: this stores the [sklearn column transformer](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html) needed to preprocess the data for the LambdaRank model.
* Query_Templat.qsf: the template QSF file
* ranker_041425.txt: the stored LambdaRank file with the trained model
* README.md: you are right now!
* requirements.txt: the file with the python packages needed, generated using pipfreeze
* skyeler_ranking_data.csv: my ranking data formatted nicely
* Star_Trek_Fillable.qsf: the qualtrics form file to be filled in.

#### Folders Overview
* The dev_files folder has old files, that are not relevant
* The embed_brokendown folder has the embeddings dataframe generated in sent_emb.ipynb broken into smaller chunks (which is done in break_it_up.ipynb).
* The sentiment_brokendown folder has the sentiment dataframe generated in sent_emb.ipynb broken down into smaller chunks (which is done in break_it_up.ipynb).
* The Evaluation folder has the qsf files and the results from the Qualtrics survey.
* The images folder has different versions of saved charts. 

### Data Access Statement 📊

The ranking data generated during this project is publicly available in this repository in the Evaluation/Results folder,for personal use only.

The _Star Trek: Next Generation_ and _Star Trek: Deep Space Nine_ data used in this project is publicly available in the [Star Trek Script Data](https://github.com/scmcqueen/StarTrekScriptData) repository, for personal use only.

