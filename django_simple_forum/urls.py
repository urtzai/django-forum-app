from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'django_simple_forum.views.index', name='forum-index'),
    url(r'^(\d+)/$', 'django_simple_forum.views.forum', name='forum-detail'),
    url(r'^topic/(\d+)/$', 'django_simple_forum.views.topic', name='topic-detail'),
    url(r'^reply/(\d+)/$', 'django_simple_forum.views.post_reply', name='reply'),
    url(r'newtopic/(\d+)/$', 'django_simple_forum.views.new_topic', name='new-topic'),
)
