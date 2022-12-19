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
import json

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')






#==========================================================================
#            FUNCTION TO CLEAN THE TEXT
#==========================================================================    
def clean_sentence(x,special_character_removal,new_stop_words,lemmatizer):
    x_ascii = unidecode(x)
    x_clean = special_character_removal.sub('',x_ascii)    
    x_clean=str(x_clean).lower()
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
def caluculate_1st_person_ratio(text,pronouns_list):
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

def get_sentiment(text,tokenizer,loaded_model_sentiments):  
    x_test_pad=pad_sequences(text,maxlen=80,padding='post')
    y_pred=loaded_model_sentiments.predict_classes(x_test_pad)
    sentiment=y_pred
    return sentiment     
#==========================================================================
#            END OF ALL SUB-FUNCTIONS
#==========================================================================  


def analyse_sentence(text):
    with open('data_light/saved_tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    loaded_model_sentiments = load_model('data_light/lstm_model.h5')
    loaded_model_toxicity= pickle.load(open('data_light/nb_tfidf.sav', 'rb'))

    pronouns_list=['i', 'we', 'you', 'he', 'she', 'they']  # list of pronouns
    special_character_removal = re.compile(r'[^A-Za-z\.\-\?\!\,\#\@\% ]',re.IGNORECASE)
    stop_words = set(stopwords.words("english"))
    exclude_words = set(pronouns_list)
    lemmatizer = WordNetLemmatizer()
    new_stop_words = stop_words.difference(exclude_words)


    total_words_body = len(text.split())
    clean_text = clean_sentence(text,special_character_removal,new_stop_words,lemmatizer)
    ratio_1st_person = caluculate_1st_person_ratio(text,pronouns_list)
    text_seq=tokenizer.texts_to_sequences(clean_text)
    predicted_sentiment = get_sentiment(text_seq,tokenizer,loaded_model_sentiments)
    predicted_toxicity = loaded_model_toxicity.predict([clean_text])
    resp = {'total_words_body':int(total_words_body),'ratio_1st_person':float(ratio_1st_person),'predicted_sentiment':[int(x) for x in predicted_sentiment],'predicted_toxicity':int(list(predicted_toxicity)[0])}
    return json.dumps(resp)


