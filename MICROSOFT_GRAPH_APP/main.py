# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>
from requests_oauthlib import OAuth2Session
import msal
from msal import PublicClientApplication
import webbrowser
import requests
import json
import pandas as pd


from sqlalchemy import create_engine

import pymysql
import psycopg2
from sqlalchemy.types import Text, VARCHAR
import pandas as pd

graph_url = "https://graph.microsoft.com/v1.0/"
APPLICATION_ID = "780f1103-8759-4406-8089-95d4d989c945"
CLIENT_SECRET = "e2T8Q~Nd6F-CsqEwH7_1MgmRn.EHJ4a5tI1eQaOZ"
authority_url = "https://login.microsoftonline.com/consumers/"
endpoint = graph_url + "me"

SCOPES = [
    "User.Read",
    "User.Export.All",
    "Mail.Read",
    "Mail.Read.Shared",
    "Mail.ReadBasic",
    "Mail.ReadWrite",
]  # "Mail.Read.Shared"


def api_call2(token, method, params={}, headers={}, graph_api_version="v1.0"):
    graph_url = "https://graph.microsoft.com/{0}".format(graph_api_version)
    headers["Authorization"] = "Bearer " + token
    response = requests.get(
        "{0}/{1}".format(graph_url, method), params=params, headers=headers
    )
    return response.json()


def api_call(token, method, params={}, headers={}, graph_api_version="v1.0"):
    graph_url = "https://graph.microsoft.com/{0}".format(graph_api_version)
    graph_client = OAuth2Session(token=token)
    response = graph_client.get(
        "{0}/{1}".format(graph_url, method), params=params, headers=headers
    )
    return response.json()


def get_user(token):
    graph_client = OAuth2Session(token=token)
    # Send GET to /me
    user = graph_client.get("{0}/me".format(graph_url))
    # Return the JSON result
    return user.json()


# </FirstCodeSnippet>

# <GetCalendarSnippet>
def get_calendar_events(token):
    # graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results
    params = {
        "$select": "subject,body,organizer,attendees,start,end",
        "$orderby": "createdDateTime DESC",
    }
    headers = {"Prefer": 'outlook.body-content-type="text"'}

    # Send GET to /me/events
    # events = graph_client.get('{0}/me/events'.format(graph_url))
    # Return the JSON result
    return api_call(token, "me/events", params=params, headers=headers)


# </GetCalendarSnippet>


# <GetEmailSnippet>
def get_emails(token):
    params = {
        # "$select": "sender,subject,body,ccRecipients,toRecipients,importance",
        # "Prefer": "outlook.body-content-type=text",
        # "top": 100,
    }
    # headers = {"Prefer": 'outlook.body-content-type="text"'}
    headers = {}
    return api_call2(token, "me/messages", params=params, headers=headers)


# </GetEmailsSnippet>


def get_ms_user_list(token):
    return api_call(token, "users")


def get_ms_teams(token):
    return api_call(token, "me/joinedTeams")


def get_ms_teams_channels(token, team_id):
    return api_call(token, "teams/{0}/channels".format(team_id))


def get_ms_teams_channels_messages(token, team_id, channel_id):
    return api_call(
        token,
        "teams/{0}/channels/{1}/messages".format(team_id, channel_id),
        graph_api_version="beta",
    )


def get_ms_teams_channel_members(token, team_id, channel_id):
    return api_call(
        token,
        "teams/{0}/channels/{1}/members".format(team_id, channel_id),
        graph_api_version="beta",
    )


client_instance = msal.ConfidentialClientApplication(
    client_id=APPLICATION_ID, client_credential=CLIENT_SECRET, authority=authority_url
)

authority_request_url = client_instance.get_authorization_request_url(SCOPES)
# webbrowser.open(authority_request_url, new=True)

authorization_code = "M.R3_BL2.6c24ff38-02f6-a3f2-2944-8406aa57261e"
access_token = client_instance.acquire_token_by_authorization_code(
    code=authorization_code, scopes=SCOPES
)
if "error" in access_token.keys():
    # print(access_token)
    with open(file="token.json", mode="r") as openfile:
        access_token = json.load(openfile)
else:
    with open(file="token.json", mode="w") as outfile:
        json.dump(access_token, outfile)

access_token_id = access_token["access_token"]


headers = {"Authorization": "Bearer " + access_token_id}
response = requests.get(endpoint, headers=headers)
print(response.json())


dt = pd.DataFrame(get_emails(access_token_id)["value"])
print(dt.columns)
print(dt.toRecipients)
