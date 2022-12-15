from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import json
from dataframe_sentiment_analysis import analysis
from sentence_analysis import analyse_sentence

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Email(BaseModel):
    id: int
    text: str
    employee: int
    subject: str
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/sentiment/classifysentence")
def predict_sentiment(email: Email):
    return analyse_sentence(email)

@app.post("/sentiment/classifydf")
def predict_sentiment_df(df_in: str):
    df = pd.DataFrame.read_json(df_in)
    df = analysis(df)
    return {"result_dataframe": df.to_json()}


    # uvicorn main:app --reload




# #fastapi
# @app.post("/receive_df")
# def receive_df(df_in: str):
#     df = pd.DataFrame.read_json(df_in)

# #jupyter
# payload={"df_in":df.to_json()}
# requests.post("localhost:8000/receive_df", data=payload)




# class Email(BaseModel):
#     id:
#     text:
#     employee: 
#     received_datetime:
#     sent_datetime:
#     has_attachments:
#     subject:
#     is_read:
#     is_draft:
#     from_name:
#     from_email:
#     to_recipients:
#     cc_recipients:
#     bcc_recipients:
#     reply_to:
#     if_forwarded:
#     created_at:
#     updated_at:



# id
# email_id 1:1
# Ratio of 1st person to 3rd person pronoun of messages 
# Message Length
# is_night_time
# is_holiday
# is_weekend
# emotion_vector
# importance: with respect to hierarchy  ---- need
# is_demand
# is_resource
# is_structured
# Number of people to whom the email was sent
# Number of people to whom cc/bcc the email was sent
# sender_is_external
# receiver_is_external
