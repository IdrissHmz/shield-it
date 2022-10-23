import requests

slack_url = 'https://slack.com/api/'
parameter = {'token':'xoxp-442542412359-442848112518-1005259561252-ece134a36a9fed25ff0d388cca819ef6'}

def api_call(method):
    response = requests.get(url=slack_url+method, params=parameter)
    return response.json()

def get_slack_users():
    return api_call('users.list')
    
def get_slack_channels():
    return api_call('users.conversations')

def get_slack_channel_info(channel):
    parameter['channel'] = channel
    return api_call('conversations.info')

def get_slack_channel_members(channel):
    parameter['channel'] = channel
    return api_call('conversations.members')

def get_slack_channel_history(channel):
    parameter['channel'] = channel
    return api_call('conversations.history')

def get_slack_team_info():
    return api_call('team.info')
