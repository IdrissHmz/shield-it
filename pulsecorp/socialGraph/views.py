from django.shortcuts import render, redirect
from django.forms import forms, fields
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.db.models import Q, Max, Count
import json
import csv
import random
import pandas as pd
from datetime import datetime
import os
from django.conf import settings
from .models import *
# from .ai_model import *
# from .topic_model import *
from pathlib import Path

from socialGraph.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from .graph_helper import get_user, get_calendar_events, get_emails, get_ms_user_list, get_ms_teams, get_ms_teams_channels, get_ms_teams_channels_messages, get_ms_teams_channel_members
import dateutil.parser
from .slack_helper import get_slack_users, get_slack_channels, get_slack_channel_info,get_slack_channel_history,get_slack_channel_members, get_slack_team_info
from jira import JIRA
#from .JiraAPIWrapper import Jira as JiraAPIWrapper
from .AESCipher import AESCipher, hash_email, hash_email_verify

#jw = JiraAPIWrapper()
aes_cipher = AESCipher(settings.SECRET_KEY)


# Create your views here.

# class MappingForm(forms.Form):
#     organization = Organization.objects.all()
#     department = Department.objects.all()
#     medium = Medium.objects.all()
#     source = fields.CharField()
#     target = fields.CharField()


class FileUploadForm(forms.Form):
    file = forms.FileField()

class FilterForm(forms.Form):
    department = Department.objects.all()

@login_required
def index(request):
    data, moral_data, status_data, collaboration_data = {}, [], [], []
    # status_obj = TaskSummary.objects.values('status').annotate(status_count=Count('status'))
    # for status in status_obj:
    #     status_data.append({"label":status['status'], "value":status['status_count']})

    moral_obj = KPISummary.objects.get(KPI_name='moral')
    moral_data.extend([
        {'label':'Very Good', 'value':moral_obj.vgood},
        {'label':'Good', 'value':moral_obj.good},
        {'label':'Neutral', 'value':moral_obj.neutral},
        {'label':'Bad', 'value':moral_obj.bad},
        {'label':'Very Bad', 'value':moral_obj.vbad}
    ])

    status_obj = KPISummary.objects.get(KPI_name='productivity')
    status_data.extend([
        {'label':'Very Good', 'value':status_obj.vgood},
        {'label':'Good', 'value':status_obj.good},
        {'label':'Neutral', 'value':status_obj.neutral},
        {'label':'Bad', 'value':status_obj.bad},
        {'label':'Very Bad', 'value':status_obj.vbad}
    ])

    collaboration_obj = KPISummary.objects.get(KPI_name='collaboration')
    collaboration_data.extend([
        {'label':'Very Good', 'value':collaboration_obj.vgood},
        {'label':'Good', 'value':collaboration_obj.good},
        {'label':'Neutral', 'value':collaboration_obj.neutral},
        {'label':'Bad', 'value':collaboration_obj.bad},
        {'label':'Very Bad', 'value':collaboration_obj.vbad}
    ])
    
    data['status_data'] = status_data
    data['moral_data'] = moral_data
    data['collaboration_data'] = collaboration_data
    return render(request,'index.html', { 'data': data })
    
def team_productivity(request):
    data = []
    status_obj = TaskSummary.objects.values('status').annotate(status_count=Count('status'))
    for status in status_obj:
        data.append({"label":status['status'], "value":status['status_count']})
    return render(request, 'team_productivity.html', { 'status_data': data })
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

@login_required
def socialGraph(request):
    if 'department_id' in request.GET and request.GET['department_id'] != '':
        selected_department = Department.objects.get(pk=request.GET['department_id'])
        persons = person.objects.filter(department=selected_department)
        communications = communication.objects.filter(Q(source__in=persons) | Q(target__in=persons))

        source = communication.objects.filter(Q(source__in=persons) | Q(target__in=persons)).values_list('source', flat=True)
        target = communication.objects.filter(Q(source__in=persons) | Q(target__in=persons)).values_list('target', flat=True)
        persons = person.objects.filter(Q(pk__in=source) | Q(pk__in=target)).distinct()
        
    else:
        persons = person.objects.all()
        communications = communication.objects.all()
    
    nodes, links, data = [], [], {}

    for p in persons:
        total_comunications = communication.objects.filter(Q(target=p) | Q(source=p)).count()
        nodes.append({'id': str(p), 'n': total_comunications, 'group': str(p.department)})

    for c in communications:
        links.append({'source': str(c.source), 'target': str(c.target)})
    
    data.update({'nodes': nodes})
    data.update({'links': links})
    form = FilterForm()

    return render(request, 'social_graph.html', {'data' : json.dumps(data), "form" : form} )

@login_required
def arc_diagram(request):
    if 'department_id' in request.GET and request.GET['department_id'] != '':
        selected_department = Department.objects.get(pk=request.GET['department_id'])
        persons = person.objects.filter(department=selected_department)
        communications = communication.objects.filter(Q(source__in=persons) & Q(target__in=persons))
    
    else:
        persons = person.objects.all()
        communications = communication.objects.all()

    nodes, links, data = [], [], {}
    
    for p in persons:
        total_comunications = communication.objects.filter(Q(target=p) | Q(source=p)).count()

        nodes.append({'name': str(p), 'id': str(p), 'n': total_comunications, 'grp': str(p.department)})

    for c in communications:
        links.append({'source': str(c.source), 'target': str(c.target)})
    
    data.update({'nodes': nodes})
    data.update({'links': links})
    form = FilterForm()

    return render(request, 'arc_diagram.html', {'data' : json.dumps(data), "form" : form} )

@login_required
def directed_graph(request):
    if 'department_id' in request.GET and request.GET['department_id'] != '':
        selected_department = Department.objects.get(pk=request.GET['department_id'])
        persons = person.objects.filter(department=selected_department)
        communications = communication.objects.filter(Q(source__in=persons) & Q(target__in=persons))
    
    else:
        persons = person.objects.all()
        communications = communication.objects.all()

    nodes, links, data = [], [], {}
    
    for p in persons:
        total_comunications = communication.objects.filter(Q(target=p) | Q(source=p)).count()

        nodes.append({'name': str(p), 'id': str(p), 'n': total_comunications/50, 'grp': str(p.department)})

    for c in communications:
        links.append({'source': str(c.source), 'target': str(c.target)})
    
    data.update({'nodes': nodes})
    data.update({'links': links})
    form = FilterForm()

    return render(request, 'directed_graph.html', {'data' : json.dumps(data), "form" : form} )

@login_required
def organization_graph(request):
    return render(request,'organization.html')
    
@csrf_exempt
@login_required
def upload_communication_list(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():

                myfile = request.FILES['file']
                fs = FileSystemStorage(location='import') #defaults to   MEDIA_ROOT  
                filename = fs.save(myfile.name, myfile)
                file_path = fs.location+"/"+filename
                header_list = list(pd.read_csv(file_path).head(0))
                
                form_mapping = MappingForm()
                return render(request,
                    'mapping.html', 
                    {'form': form_mapping, 'header_list':header_list, 'file_path': file_path}
                )
        elif 'file_path' in request.POST:
            persons = []
            file_path = request.POST['file_path']
            # medium_id = request.POST['medium']
            # organization_id = request.POST['organization']
            # department_id = request.POST['department']
            source = request.POST['source']
            target = request.POST['target']
            data = pd.read_csv(file_path)
            source_list = list(data[source].unique())
            target_list = list(data[target].unique())
            persons.extend(source_list)
            persons.extend(target_list)
            departments = Department.objects.all()
            organizations = Organization.objects.all()
            mediums = Medium.objects.all()
            
            for p in persons:
                print(p)
                name = p.split('@')

                if not person.objects.filter(email=p).count():
                    obj = person.objects.create(
                        email=p, 
                        name=name[0],
                        organization=random.choice(organizations),
                        department=random.choice(departments)
                        )
                    print('created')
            links = data[[source, target]]
            print(links)
            for i, j in links.iterrows():
                print(i, j)
                communication.objects.create(
                    source=person.objects.get(email=j[source]),
                    target=person.objects.get(email=j[target]),
                    medium=random.choice(mediums),
                    subject='test',
                    body='test'
                    )
            return redirect(index)
    else:
        form = FileUploadForm()
    return render(request, 'file-upload-form.html', {'form': form})


# <HomeViewSnippet>
def home(request):
  context = initialize_context(request)

  return render(request, 'MS/home.html', context)
# </HomeViewSnippet>

# @csrf_exempt
# def ai_demo(request):
#     context = initialize_context(request)
#     if request.POST:
#         print("Demo")
#         sentiment, topic = ai_demo_prediction(request.POST['text'])
#         # print(topic)
#         print(sentiment)
#         return JsonResponse(
#                 {
#                     'sentiment':sentiment,
#                     'topic': topic
#                 }
#             )

#     return render(request, 'MS/ai_demo.html', context)
# <InitializeContextSnippet>
def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context
# </InitializeContextSnippet>

# <SignInViewSnippet>
def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)
# </SignInViewSnippet>

# <SignOutViewSnippet>
def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('socialGraph:home'))
# </SignOutViewSnippet>

# <CallbackViewSnippet>
def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('socialGraph:home'))
# </CallbackViewSnippet>

# <CalendarViewSnippet>
def calendar(request):
  context = initialize_context(request)
  token = get_token(request)
  events = ms_calendar_insertion(token)
  
  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'MS/calendar.html', context)
# </CalendarViewSnippet>

# <EmailViewSnippet>
def email(request):
    context = initialize_context(request)
    token = get_token(request)
    
    users = ms_user_insertion(token)
    emails = ms_email_insertion(token)
    ms_team = ms_team_insertion(token)
  
    if emails:
        context['emails'] = emails['value']

    return render(request, 'MS/email.html', context)
# </EmailViewSnippet>

# <ProjectlViewSnippet>
def project(request):
    context = initialize_context(request)
    jira_insertion()
    projects = jw.getProjects()
    if projects:
        context['projects'] = projects
    return render(request, 'MS/project.html', context)
# <ProjectViewSnippet>


# <ProjectlViewSnippet>
def issue(request):
  project_key = request.GET['project_key']
  context = initialize_context(request)
  issues = jw.getIssues(project=project_key, raw=True)
  print(issues)
  if issues:
    context['issues'] = issues
  
  return render(request, 'MS/issue.html', context)
# <ProjectViewSnippet>


def slack_users(request):
    context = initialize_context(request)
    slack_users = get_slack_channels()
    slack_user_insertion()
    slack_channel_insertion()

    if slack_users:
        context['slack_users'] = slack_users
    return render(request, 'MS/slack_users.html', context)

def slack_user_insertion():
    slack_team = get_slack_team_info()
    slack_team_id = slack_team['team']['id']
    slack_team_name = slack_team['team']['name']
    slack_team_obj, created = SlackTeam.objects.get_or_create(
        slack_team_id=slack_team_id,
        name=slack_team_name
    )

    slack_users = get_slack_users()
    for member in slack_users['members']:
        slack_id = member['id']
        team_id = member['team_id'] 
        name = member['profile']['real_name'].split(' ')
        if 'email' in member['profile'] and member['profile']['email']:
            user_obj = insert_user(
                id=member['id'], 
                email=member['profile']['email'], 
                first_name=name[0], 
                last_name=name[1] if len(name)>1 else '', 
                title=member['profile']['title'], 
                medium='slack'
            )
            slack_user_obj, created = slackUser.objects.get_or_create(
                user=user_obj,
                slack_team=slack_team_obj
            )

def slack_channel_insertion():
    slack_channels = get_slack_channels()

    for channel in slack_channels['channels']:
        name = channel['name']
        slack_channel_id = channel['id']
        creator = UserProfileInfo.get_user_with_slack_key(channel['creator'])
        slack_channel_datetime = datetime.utcfromtimestamp(channel['created']).strftime('%Y-%m-%d %H:%M:%S')
        slack_team = SlackTeam.get_slack_team_with_key(channel['shared_team_ids'][0])
        slack_channel_obj, created = SlackChannel.objects.get_or_create(
            name=name,
            slack_channel_id=slack_channel_id,
            creator=creator,
            slack_team=slack_team
        )

        topic_text = channel['topic']['value']
        purpose_text = channel['purpose']['value']

        if topic_text:
            slack_channel_desc_obj, created = SlackChannelDescription.objects.get_or_create(
                slack_channel_description='topic',
                text=topic_text,
                slack_channel=slack_channel_obj,
                creator=UserProfileInfo.get_user_with_slack_key(channel['topic']['creator']),
            )
        if purpose_text:
            slack_channel_desc_obj, created = SlackChannelDescription.objects.get_or_create(
                slack_channel_description='purpose',
                text=purpose_text,
                slack_channel=slack_channel_obj,
                creator=UserProfileInfo.get_user_with_slack_key(channel['purpose']['creator']),
            )

        slack_channel_members = get_slack_channel_members(slack_channel_id)
        for member in slack_channel_members['members']:
            slack_channel_member_obj, created = SlackChannelMember.objects.get_or_create(
                user=UserProfileInfo.get_user_with_slack_key(member),
                slack_channel=slack_channel_obj
            )
        
        slack_channel_messages = get_slack_channel_history(slack_channel_id)
        for message in slack_channel_messages['messages']:
            if 'client_msg_id' in message:
                try:
                    sender = UserProfileInfo.get_user_with_slack_key(message['user'])
                    slack_channel_members_obj = SlackChannelMember.objects.filter(slack_channel=slack_channel_obj)
                    slack_channel_message_object, created = SlackMessage.objects.get_or_create(
                        slack_message_id=message['client_msg_id'],
                        text=message['text'],
                        user=sender,
                        slack_team=SlackTeam.get_slack_team_with_key(message['team']),
                        slack_channel=slack_channel_obj,
                        content_type=ContentType.objects.get(pk=1),
                        size=len(message['text'].split()),
                        to_team=check_team_related(slack_channel_members_obj, sender)
                    )
                except User.DoesNotExist as e:
                    slack_channel_message_object = None
                    print(e)
                    continue
                if slack_channel_message_object is not None and created:
                    for member in slack_channel_members_obj:
                        SlackMessageRecipient.objects.get_or_create(
                            recipient_type='cm',
                            user=member.user,
                            slack_message=slack_channel_message_object,
                            from_team=member.user.userprofileinfo.department==sender.userprofileinfo.department
                        )

def check_team_related(members, sender):
    for member in members:
        try:
            if member.user.userprofileinfo.department == sender.userprofileinfo.department:
                return True
        except User.DoesNotExist as e:
            print(e)
    return False

def jira_insertion():
    users = User.objects.all()
    for user in users:
        if user.email:
            email_left = user.email.split('@')[0]
            email_right = user.email.split('@')[1]
            jira_user = jw.search_users(query=aes_cipher.decrypt(email_left)+'@'+email_right)
            if jira_user:
                user_medium_obj, created = UserMedium.objects.get_or_create(
                    user=user,
                    user_key=jira_user[0]['accountId'],
                    medium=Medium.objects.get(name='jira')
                )
    projects = jw.getProjects()
    for project in projects:
        jira_project_obj , created = JiraProject.objects.get_or_create(
            name=project['name'],
            Key=project['key'],
            jira_id=project['id']
        )
        issues = jw.getIssues(project=project['key'])

        if issues:
            for issue in issues:
                if 'assignee' in issue and issue['assignee'] is not None:
                    assignee = UserProfileInfo.get_user_with_jira_key(issue['assignee'].accountId)
                    reporter = UserProfileInfo.get_user_with_jira_key(issue['reporter'].accountId)
                    
                    if assignee is not None and reporter is not None:
                        issue_obj, created = JiraIssue.objects.get_or_create(
                            assignee=assignee,
                            status=issue['status'],
                            reporter=reporter,
                            name=issue['name'],
                            summary=issue['summary'],
                            description=issue['description'],
                            jira_project=jira_project_obj
                        )

def ms_user_insertion(token):
    users = get_ms_user_list(token)
    for user in users['value']:
        if user['mail'] is not None:
            insert_user(
                id=user['id'], 
                email=user['mail'], 
                first_name=user['givenName'], 
                last_name=user['surname'], 
                title=user['jobTitle'] if user['jobTitle'] is not None else '', 
                medium='microsoft'
            )
    return users

def insert_user(id, email, first_name, last_name, title, medium):
    email_left = email.split('@')[0]
    email_right = email.split('@')[1]
    user_obj, created = User.objects.get_or_create(username=hash_email(email))
    if created:
        user_obj.email=aes_cipher.encrypt(email_left)+'@'+email_right
        user_obj.save()
        
        # email_hash = hash_email(email)
        # test = hash_email_verify(email, email_hash)
        user_profile_obj = UserProfileInfo.objects.create(
            user = user_obj,
            first_name = aes_cipher.encrypt(first_name),
            last_name = aes_cipher.encrypt(last_name),
            job_title=title,
            organization=Organization.objects.get(pk=1),
            department=Department.objects.get(pk=1)
        )
    else:
        user_profile_obj = UserProfileInfo.objects.get(user = user_obj)
        user_profile_obj.first_name = first_name if not user_profile_obj.first_name else user_profile_obj.first_name
        user_profile_obj.last_name = last_name if not user_profile_obj.last_name else user_profile_obj.last_name
        user_profile_obj.job_title=title if not user_profile_obj.job_title else user_profile_obj.job_title
        user_profile_obj.save()

    user_medium_obj, created = UserMedium.objects.get_or_create(
        user=user_obj,
        user_key=id,
        medium=Medium.objects.get(name=medium)
    )
    return user_obj

def ms_email_insertion(token):
    emails = get_emails(token)
    for email in emails['value']:
        if 'sender' in email and 'address' in email['sender']['emailAddress']:
            sender =  email['sender']['emailAddress']['address']
            try:
                sender = User.objects.get(username=hash_email(sender))
            except User.DoesNotExist as e:
                print(e)
                continue
            try:
                email_obj, created = MSEmail.objects.get_or_create(
                    sender=sender,
                    subject=email['subject'] if email['subject'] else '',
                    body=email['body']['content'].encode('unicode_escape').decode("utf-8") if email['body']['content'] else '',
                    importance = email['importance'],
                    size=len(email['body']['content'].encode('unicode_escape').decode("utf-8").split()),
                    to_team=check_team_related_email(email['toRecipients'], sender)
                )
            except User.DoesNotExist as e:
                email_obj = None
                print(e)
                continue
            if email_obj is not None and created:
                for toRecipient in email['toRecipients']:
                    if 'address' in toRecipient['emailAddress']:
                        try:
                            user = User.objects.get(username=hash_email(toRecipient['emailAddress']['address']))
                            to_recipient_obj = MSEmailRecipient.objects.get_or_create(
                                email=email_obj,
                                recipient_type='to',
                                user=user,
                                from_team=user.userprofileinfo.department==sender.userprofileinfo.department
                            )
                        except User.DoesNotExist as e:
                            print(e)

                for ccRecipient in email['ccRecipients']:
                    if 'address' in ccRecipient['emailAddress']:
                        try:
                            user = User.objects.get(username=hash_email(ccRecipient['emailAddress']['address']))
                            to_recipient_obj = MSEmailRecipient.objects.get_or_create(
                                email=email_obj,
                                recipient_type='cc',
                                user=user,
                                from_team=user.userprofileinfo.department==sender.userprofileinfo.department
                            )
                        except User.DoesNotExist as e:
                            print(e)
    return emails

def check_team_related_email(toRecipients, sender):
    for toRecipient in toRecipients:
        if 'address' in toRecipient['emailAddress']:
            try:
                user = User.objects.get(username=hash_email(toRecipient['emailAddress']['address']))
                if user.userprofileinfo.department == sender.userprofileinfo.department:
                    return True
            except User.DoesNotExist as e:
                print(e)
    return False

def ms_team_insertion(token):
    ms_teams = get_ms_teams(token)
    for ms_team in ms_teams['value']:
        ms_team_id = ms_team['id']
        ms_team_obj, created = MSTeam.objects.get_or_create(
            ms_id = ms_team_id,
            name=ms_team['displayName']
        )
        ms_team_channels = get_ms_teams_channels(token, ms_team_id)
        for channel in ms_team_channels['value']:
            ms_team_channel_id = channel['id']
            ms_team_channel_obj, created = MSTeamChannel.objects.get_or_create(
                ms_id=ms_team_channel_id,
                name=channel['displayName'],
                description=channel['description'],
                ms_team=ms_team_obj
            )


            ms_team_channel_members = get_ms_teams_channel_members(token, ms_team_id, ms_team_channel_id)
            for member in ms_team_channel_members['value']:
                try: 
                    user = UserProfileInfo.get_user_with_ms_key(member['userId'])
                    if user is not None:
                        ms_team_channel_member_obj, created = MSTeamChannelMember.objects.get_or_create(
                            user=UserProfileInfo.get_user_with_ms_key(member['userId']),
                            ms_team_channel=ms_team_channel_obj
                        )
                except User.DoesNotExist as e:
                    print(e)

            ms_team_channel_messages = get_ms_teams_channels_messages(token, ms_team_id, ms_team_channel_id)
            for msg in ms_team_channel_messages['value']:
                try:
                    sender = UserProfileInfo.get_user_with_ms_key(msg['from']['user']['id'])
                    ms_team_channel_members_obj = MSTeamChannelMember.objects.filter(ms_team_channel=ms_team_channel_obj)
                    ms_msg_type_obj, new = MSTeamMessageType.objects.get_or_create(message_type=msg['messageType'])
                
                    msg_obj, created = MSTeamMessage.objects.get_or_create(
                    ms_message_id = msg['id'],
                    text=msg['body']['content'],
                    user=sender,
                    ms_team=ms_team_obj,
                    ms_team_channel=ms_team_channel_obj,
                    ms_team_message_type=ms_msg_type_obj,
                    content_type=ContentType.objects.get(pk=1),
                    size=len(msg['body']['content'].split()),
                    to_team=check_team_related(ms_team_channel_members_obj, sender)
                    )

                except User.DoesNotExist as e:
                    msg_obj = None
                    print(e)
                    continue
                if msg_obj is not None and created:
                    for member in ms_team_channel_members_obj:
                        MSTeamMessageRecipient.objects.get_or_create(
                            recipient_type='cm',
                            user=member.user,
                            ms_team_message=msg_obj,
                            from_team=member.user.userprofileinfo.department==sender.userprofileinfo.department
                        )
                    
    return ms_teams

def ms_calendar_insertion(token):
    events = get_calendar_events(token)

    for event in events['value']:
        if 'address' in event['organizer']['emailAddress']:
            try:
                ms_calendar_obj, created = MSCalendar.objects.get_or_create(
                    subject=event['subject'],
                    body=event['body']['content'],
                    organizer = User.objects.get(username=hash_email(event['organizer']['emailAddress']['address']))
                )
            except User.DoesNotExist as e:
                ms_calendar_obj = None
                print(e)

            if ms_calendar_obj is not None and created:
                for attendee in event['attendees']:
                    if 'address' in attendee['emailAddress']:
                        try:
                            ms_calendar_attendee_obj, created = MSCalendarAttendees.objects.get_or_create(
                                attendee=User.objects.get(username=hash_email(attendee['emailAddress']['address'])),
                                ms_calendar=ms_calendar_obj,
                                response=attendee['status']['response'] if attendee['status']['response'] is not None else ''
                            )
                        except User.DoesNotExist as e:
                            print(e)
    return events

# def ai_demo_prediction(text):
#     test_set = pd.DataFrame(columns=['id', 'sentence'])
#     test_set['sentence']= [text]
#     test_set['id'] = 1
#     data_pred = test_set #pd.read_csv('/kaggle/working/train.csv')
#     data_pred = data_pred.fillna('')  # only the comments has NaN's
#     rws_pred = data_pred.sentence # give column name which have data like (data.abstract for covid data)


#     os.system("echo Hello")
#     file1 = open('topic_model_text.txt', 'w')
#     file1.write(test_set['sentence'][0])
#     file1.close()

#     os.system("conda activate nlp-env36 && python socialgraph/topic_model.py")
#     result_topic = Path('topic_model_result.txt').read_text()


    
#     # Preprocessing for new data uncomment
#     # start_time = time.time()
#     # sentences, token_lists, idx_in = preprocess(rws_pred, samp_size=1)
#     # results_tm = get_prediction_tm(model_tm, sentences, token_lists)
#     # result = mydict[results_tm]

#     test_dataloader, input_id_dict = data_preprocess(test_set)
#     bert_result_df = bert_prediction(test_dataloader, input_id_dict)
    
#     # result_df = pd.merge(bert_result_df, top1_topic_df, on='id')
#     # print(result_df)
#     # results = result_df.to_dict('records')
#     return  bert_result_df['BERT_prediction'][0], result_topic

# def AI_function(request):
#     test_set = pd.DataFrame(list(MSEmail.objects.filter(ai_status=False).values()))
#     test_set.rename(columns={'body':'sentence'}, inplace=True)
#     print(test_set)

#     top1_topic_df = pd.DataFrame(columns=['id', 'LDA_prediction'])

#     # variables
#     samp_size = len(test_set)

    # data_pred = test_set #pd.read_csv('/kaggle/working/train.csv')
    # data_pred = data_pred.fillna('')  # only the comments has NaN's
    # rws_pred = data_pred.sentence # give column name which have data like (data.abstract for covid data)
    
    # # Preprocessing for new data uncomment
    # start_time = time.time()
    # sentences, token_lists, idx_in = preprocess(rws_pred, samp_size=samp_size)
    # print("Data Prepprocessing time--- %s seconds ---\n" % (time.time() - start_time))
    
#     # Get LDA+BERT topic model predictions
#     results_tm = get_prediction_tm(model_tm, sentences, token_lists)
# #     print(top1_topic_df)
#     # get topic names
#     results_tm_name = []
#     for  i in results_tm:
#         results_tm_name.append(mydict[i])
#     print("results and results name: ", results_tm, results_tm_name)
#     top1_topic_df['id'] = test_set['id']
#     top1_topic_df['LDA_prediction'] = results_tm_name
    
#     test_dataloader, input_id_dict = data_preprocess(test_set)
#     bert_result_df = bert_prediction(test_dataloader, input_id_dict)
    
#     result_df = pd.merge(bert_result_df, top1_topic_df, on='id')
#     print(result_df)
#     results = result_df.to_dict('records')
#     for result in results:
#         print(result['id'])
#         MSEmail.objects.filter(pk=result['id']).update(
#             ai_predicted_topic=result['LDA_prediction'],
#             ai_predicted_sentiment=result['BERT_prediction'],
#             ai_status = True
#             )
