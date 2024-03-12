from django.urls import re_path
from django_forum_app import views

urlpatterns = [
    re_path(r'^$', views.index, name='forum-index'),
    re_path(r'^(?P<slug>[-\w]+)/$', views.forum, name='forum-detail'),
    re_path(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/$', views.topic, name='topic-detail'),
    re_path(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/close$', views.close_topic, name='close-topic'),
    re_path(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/reply/$', views.post_reply, name='reply'),
    re_path(r'(?P<slug>[-\w]+)/newtopic/$', views.new_topic, name='new-topic'),
]
