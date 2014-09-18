from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'django_simple_forum.views.index', name='forum-index'),
    url(r'^(?P<slug>[-\w]+)/$', 'django_simple_forum.views.forum', name='forum-detail'),
    url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/$', 'django_simple_forum.views.topic', name='topic-detail'),
    url(r'^(?P<topic_id>\d+)/reply/$', 'django_simple_forum.views.post_reply', name='reply'),
    url(r'(?P<slug>[-\w]+)/newtopic/$', 'django_simple_forum.views.new_topic', name='new-topic'),
)
