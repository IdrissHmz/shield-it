#!/usr/bin/env python
# coding: utf-8

# # LDA model Prediction Code
# Imports
from os import listdir, chdir
import re
import time
from gensim import models, corpora
import json
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
import numpy as np
import random

# new model imports
import pickle
# Preprocessing libraries
from stop_words import get_stop_words
from language_detector import detect_language
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from symspellpy import SymSpell, Verbosity
import pkg_resources

# Load ldamodel
# model_path = r'C:\nlp_project\LDAdata_results\LDAdata_results\ldamodel_a_no_name'
# ldamodel = models.LdaModel.load(model_path) 


# identify and specify the GPU as the device, later in training loop we will load data into device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_gpu = torch.cuda.device_count()
torch.cuda.get_device_name(0)
# print(n_gpu)
SEED = 19
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if device == torch.device("cuda"):
    torch.cuda.manual_seed_all(SEED)

device = torch.device("cuda")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6).to(device)
model.load_state_dict(torch.load(r'C:\nlp_project\working_bert_90k\model\fineTuneModel.pt'))
model.eval()

# ### Declare Variables
# batch size for data handeling
batch_size = 16
## emotion labels
int2label = {
    0: "anger",
    1: "fear",
    2: "joy",
    3: "love",
    4: "sadness",
    5: "surprise",
    
}


# # LDA main functions for preprocessing and prediction
# # function for preprocess
# def match_words(word):
#     wordnet_lemmatizer = WordNetLemmatizer()
#     word_edit = word.lower()
#     try:
#         word_edit = tokenizer.tokenize(word_edit)[0]
#     except:
#         pass
#     return wordnet_lemmatizer.lemmatize(word_edit)

# # function for prediction
# def read_doc(doc):
#     # Variables so recalculation is not necessary
#     doc_split = doc.split()
    
#     # Build dictionary of topic's distribution for a given document
#     num_topics_weight = 0
#     Topics = defaultdict(int)
    
#     for word in doc_split:
#         word_edit = match_words(word)    
#         try:
#             word_topics = ldamodel.get_term_topics(word_edit)
#             if word_topics:
#                 for topic in word_topics:
#                     Topics[topic[0]] += topic[1]
#                     num_topics_weight += topic[1]            
#         except:
#             pass
#     # Find topic info
#     # Append Topic, number of words in document from given topic and doc percentage of topic
#     Topic_info = []
#     for topic in Topics:
#         Topic_info.append([topic, Topics[topic], round((Topics[topic]/num_topics_weight)*100)]) 
    
#     # Topic info for three most prevalent topics for a given document
#     Topic_info_top3 = []
#     Topic_info_copy = []
#     for i in Topic_info:
#         Topic_info_copy.append(i)
    
#     for i in range(0,3):
#         max = Topic_info_copy[0]
#         for topic in Topic_info_copy:
#             if topic[2] > max[2]:
#                 max = topic
#         Topic_info_top3.append(max)
#         Topic_info_copy.remove(max)
        
#     Top1_topic = mydict.get(Topic_info_top3[0][0])

#     return Top1_topic

# # BERT Sentiment Analysis Model prediction
# ## Preprocessing
# MAke counter dictionary for input ids to keep track of batches
def make_input_ids_dict(test_inputs, ids_f):
    # make dictionary for input ids
    input_id_dict = dict()
    #     print("make_input_dict", len(test_inputs), len(ids_f))
    
    for i in range(len(test_inputs)):
        print("check : ", i, )
        input_id_dict[ids_f[i]] = test_inputs[i]
    # print(len(input_id_dict), input_id_dict)
    return input_id_dict

# function for data preprocessing
def data_preprocess(test_set):
    ## create label and sentence list
    sentences_f = test_set.sentence.values
    ids_f = test_set.id.values
    #     print(ids_f[0], sentences_f[0])
    #check distribution of data based on labels

    # Set the maximum sequence length. The longest sequence in our training set is 47, but we'll leave room on the end anyway. 
    # In the original paper, the authors used a length of 512.
    MAX_LEN = 512

    ## Import BERT tokenizer, that is used to convert our text into tokens that corresponds to BERT library
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)
    input_ids_f = [tokenizer.encode(sent, add_special_tokens=True,max_length=MAX_LEN,pad_to_max_length=True) for sent in sentences_f]
    #     print(input_ids_f[0])
    ## Create attention mask
    attention_masks = []
    ## Create a mask of 1 for all input tokens and 0 for all padding tokens
    attention_masks = [[float(i>0) for i in seq] for seq in input_ids_f]
    #     print(attention_masks[0])
    
    test_inputs = torch.tensor(input_ids_f)
    test_masks = torch.tensor(attention_masks)
    input_id_dict = make_input_ids_dict(test_inputs, ids_f)
    #     print("tensor input", test_inputs[0])
    #     print("input_id_dict", input_id_dict.loc[0])
    
    test_data = TensorDataset(test_inputs,test_masks)
    test_sampler = RandomSampler(test_data)
    test_dataloader = DataLoader(test_data,sampler=test_sampler,batch_size=batch_size)
    
    return test_dataloader, input_id_dict


# ## Prediction
# make map of the input batches
def get_input_map(batch, input_id_dict):
    input_id_map = []
    batch_input_id , _ = batch
    #     print("get input map: ", len(input_id_dict), len(batch_input_id))
    for batch_tensor in batch_input_id:
        for key, value in input_id_dict.items():
            if torch.equal(batch_tensor, value):
                input_id_map.append(key)
    return input_id_map


# Bert prediction function
def bert_prediction(test_dataloader, input_id_dict):
    # Tracking variables     
    pred_flat_list, label_str = [], []
    for batch in test_dataloader:
        # Map batch indexes in list
        input_id_map = get_input_map(batch, input_id_dict)
    
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask = batch # b_labels are true lables in batch

        # Telling the model not to compute or store gradients, saving memory and speeding up validation
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            logits = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)

        # Move logits and labels to CPU
        logits = logits[0].to('cpu').numpy()

        pred_flat = np.argmax(logits, axis=1).flatten()
        pred_flat_list.append(pred_flat)
    pred_list = np.concatenate(pred_flat_list)
    pred_list_str = []
    for i in pred_list:
        pred_list_str.append(int2label[i])
    # print("input id map", len(input_id_map), "pred list", len(pred_list_str))
    df_metrics=pd.DataFrame({'id': input_id_map, 'BERT_prediction':pred_list_str})
    return df_metrics

    
# # MAIN Function
def main():
    # load data
    test_set= pd.read_csv(r"C:\Users\Administrator\Downloads\emails_angry_new.csv", header=0, usecols=[1,2])
    test_set.rename(columns={'emails':'sentence'}, inplace=True) # modify according to input dataframe
    
    start_time = time.time()
    # predict from LDA model
    top1_topics = []
    for data in test_set['sentence']:
        top1_topics.append(read_doc(data))

    print("LDA model--- %s seconds ---\n" % (time.time() - start_time))
    
    start_time = time.time()
    # predict from BERT model
    test_dataloader, input_id_dict = data_preprocess(test_set)
    result_df = bert_prediction(test_dataloader, input_id_dict)
    
    print("BERT model--- %s seconds ---\n" % (time.time() - start_time))
    #     result_df = result_df.set_index(['Email_id'])
    result_df = result_df.sort_values('Email_id')
    
    result_df['LDA_prediction'] = top1_topics
    print(result_df)

# main()