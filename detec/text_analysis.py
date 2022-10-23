#!/usr/bin/env python
# coding: utf-8

# ## Import Necessary Libraries
import re
import string
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def analysis(df_test):
    """  

    Parameters
    ----------
    df_test : this dataframe will contain raw data filtered on the basis of 
    timeframe. That timeframe can be yearly, monthly, or daily. 

    Returns
    -------
    This function will return nothing, instead it will add columns of sentiments,
    toxicity, ratio of 1st person pronoun to other pronouns, total number of words
    in body, and clean text in same df_test

    """

    
    #==========================================================================
    #            FUNCTION TO CLEAN THE TEXT
    #==========================================================================    
    def clean_text(x):
        x_ascii = unidecode(x)
        x_clean = special_character_removal.sub('',x_ascii)    
        x_clean=x_clean.lower()
        translator = str.maketrans('', '', string.punctuation)
        x_clean=x_clean.translate(translator)
        word_tokens = word_tokenize(x_clean) 
        x_clean=" ".join(word_tokens)
        x_clean = ([word for word in word_tokens if word not in new_stop_words])
        x_clean = " ".join([lemmatizer.lemmatize(word, pos ='v') for word in x_clean])
        return x_clean
    
    #==========================================================================
    #            FUNCTION TO CALCULATE RATIO OF 1ST PERSON PRONOUN
    #==========================================================================
    def caluculate_1st_person_ratio(text):
        first_pronoun_count=0
        pronoun_count=0
        words=word_tokenize(text)
        for word in words:    
            if word in pronouns_list:
                pronoun_count=pronoun_count+1
                if word=='i' or word== 'we':            
                    first_pronoun_count=first_pronoun_count+1
        if pronoun_count==0:  # to avoid division by 0
            ratio =0
        else:
            ratio=first_pronoun_count/pronoun_count
        return ratio    
    #==========================================================================
    #            FUNCTION TO GET PREDICTED SENTIMENT
    #{'joy':0,'anger':1,'love':2,'sadness':3,'fear':4,'surprise':5}
    #==========================================================================
    
    def get_sentiment(text):  
        x_test_f=tokenizer.texts_to_sequences(text)
        x_test_pad=pad_sequences(x_test_f,maxlen=80,padding='post')
        y_pred=loaded_model_sentiments.predict_classes(x_test_pad)
        sentiment=y_pred
        return sentiment     
    #==========================================================================
    #            END OF ALL SUB-FUNCTIONS
    #==========================================================================  
    loaded_model_sentiments = load_model('data_light/lstm_model.h5')
    pronouns_list=['i', 'we', 'you', 'he', 'she', 'they']  # list of pronouns
    special_character_removal = re.compile(r'[^A-Za-z\.\-\?\!\,\#\@\% ]',re.IGNORECASE)
    stop_words = set(stopwords.words("english"))
    exclude_words = set(pronouns_list)
    lemmatizer = WordNetLemmatizer()
    new_stop_words = stop_words.difference(exclude_words)
    
      
    df_test['total_words_body']= df_test['body'].str.split().str.len()
    df_test.drop(df_test.index[df_test['total_words_body'] >1000], inplace=True) # drop rows having number of words greate than 1000 in body
    
    df_test['clean_text']=df_test['body'].apply(lambda x: clean_text(x))
    

    df_test.drop(labels='body', axis=1, inplace=True)
    
    df_test['ratio_1st_person']=df_test['clean_text'].apply(lambda x: caluculate_1st_person_ratio(x))

    with open('data_light/saved_tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

    x_test_f=tokenizer.texts_to_sequences(df_test)
    x_test_pad=pad_sequences(x_test_f,maxlen=80,padding='post')
    
    df_test['predicted_sentiment'] =  get_sentiment(df_test['clean_text'])
    loaded_model_toxicity= pickle.load(open('data_light/nb_tfidf.sav', 'rb'))
    predicted_toxicity = loaded_model_toxicity.predict(df_test.clean_text.values)
    df_test['predicted_toxicity']= predicted_toxicity
    