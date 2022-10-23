from django.urls import path
from django.conf.urls import url

from socialGraph import views

app_name = 'socialGraph'

urlpatterns = [
    path('', views.index, name='index'),
    # path('socialGraph', views.socialGraph, name='SocialGraph'),
    path('arcDiagram', views.arc_diagram, name='arc_diagram'),
    path('directedGraph', views.directed_graph, name='directed_graph'),
    path('organization', views.organization_graph, name='organization_graph'),
    path('upload', views.upload_communication_list, name='file_upload'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^socialGraph/$', views.socialGraph, name='social_graph'),
    path('teamProductivity', views.team_productivity, name='team_productivity'),

    path('home', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('callback', views.callback, name='callback'),
  path('calendar', views.calendar, name='calendar'),
  path('email', views.email, name='email'),
  path('project', views.project, name='project'),
  url(r'^issue$', views.issue, name='issue'),
  path('slackUsers', views.slack_users, name='slack_users'),
  # path('aidemo', views.ai_demo, name='ai_demo'),
]