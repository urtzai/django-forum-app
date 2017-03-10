from django.conf.urls import url
from django_forum_app import views

urlpatterns = [
    url(r'^$', views.index, name='forum-index'),
    url(r'^(?P<slug>[-\w]+)/$', views.forum, name='forum-detail'),
    url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/$', views.topic, name='topic-detail'),
    url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/close$', views.close_topic, name='close-topic'),
    url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/reply/$', views.post_reply, name='reply'),
    url(r'(?P<slug>[-\w]+)/newtopic/$', views.new_topic, name='new-topic'),
]
