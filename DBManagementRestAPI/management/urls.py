from django.urls import re_path
from management import views 
 
urlpatterns = [ 
    re_path(r'^api/users$', views.user_list),
    re_path(r'^api/users/(?P<pk>[0-9]+)$', views.user_detail),
    re_path(r'^api/mails$', views.mail_list),
    re_path(r'^api/mails/(?P<pk>[0-9]+)$', views.mail_detail),
    re_path(r'^api/(?P<pk>[0-9]+)/mails$', views.user_mails),
]