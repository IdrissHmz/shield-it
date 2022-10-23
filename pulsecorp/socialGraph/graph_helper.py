# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>
from requests_oauthlib import OAuth2Session

graph_url = 'https://graph.microsoft.com/v1.0'
APPLICATION_ID = '780f1103-8759-4406-8089-95d4d989c945'
CLIENT_SECRET = 'Qor8Q~g8099QBo3ckM2VmHdmdsSp~NYb4w5TjbN0'

def api_call(token, method, params={}, headers={}, graph_api_version='v1.0'):
  graph_url = 'https://graph.microsoft.com/{0}'.format(graph_api_version)
  graph_client = OAuth2Session(token=token)
  response = graph_client.get('{0}/{1}'.format(graph_url, method), params=params, headers=headers)
  return response.json()

def get_user(token):
  graph_client = OAuth2Session(token=token)
  # Send GET to /me
  user = graph_client.get('{0}/me'.format(graph_url))
  # Return the JSON result
  return user.json()
# </FirstCodeSnippet>

# <GetCalendarSnippet>
def get_calendar_events(token):
  # graph_client = OAuth2Session(token=token)

  # Configure query parameters to
  # modify the results
  params = {
    '$select': 'subject,body,organizer,attendees,start,end',
    '$orderby': 'createdDateTime DESC'
  }
  headers = {
    'Prefer': 'outlook.body-content-type="text"'
  }

  # Send GET to /me/events
  # events = graph_client.get('{0}/me/events'.format(graph_url))
  # Return the JSON result
  return api_call(token, 'me/events', params=params, headers=headers)
# </GetCalendarSnippet>


# <GetEmailSnippet>
def get_emails(token):
  params = {
    '$select': 'sender,subject,body,ccRecipients,toRecipients,importance',
    'Prefer': 'outlook.body-content-type=text',
    'top':100
  }
  headers = {
    'Prefer': 'outlook.body-content-type="text"'
  }

  return api_call(token, 'me/messages', params=params, headers=headers)
# </GetEmailsSnippet>

def get_ms_user_list(token):
  return api_call(token, 'users')

def get_ms_teams(token):
  return api_call(token, 'me/joinedTeams')

def get_ms_teams_channels(token, team_id):
  return api_call(token, 'teams/{0}/channels'.format(team_id))

def get_ms_teams_channels_messages(token, team_id, channel_id):
  return api_call(token,'teams/{0}/channels/{1}/messages'.format(team_id, channel_id), graph_api_version='beta')


def get_ms_teams_channel_members(token, team_id, channel_id):
  return api_call(token,'teams/{0}/channels/{1}/members'.format(team_id, channel_id), graph_api_version='beta')



