from django.template import RequestContext

from django.forms import models as forms_models

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.context_processors import csrf

from django_simple_forum.models import Forum, Topic, Post
from django_simple_forum.forms import TopicForm, PostForm

from guest.decorators import guest_allowed, login_required

from django.template import RequestContext

from settings import *

def index(request):
    """Main listing."""
    forums = Forum.objects.all()
    return render_to_response("django_simple_forum/list.html", {'forums': forums, 
                                'user': request.user}, 
                                context_instance=RequestContext(request))


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def forum(request, forum_id):
    """Listing of topics in a forum."""
    topics = Topic.objects.filter(forum=forum_id).order_by("-created")
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

    forum = get_object_or_404(Forum, pk=forum_id)

    return render_to_response("django_simple_forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum),
                              context_instance=RequestContext(request))

def topic(request, topic_id):
    """Listing of posts in a topic."""
    posts = Post.objects.filter(topic=topic_id).order_by("created")
    posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
    topic = Topic.objects.get(pk=topic_id)
    return render_to_response("django_simple_forum/topic.html", add_csrf(request, posts=posts, pk=topic_id,
        topic=topic), context_instance=RequestContext(request))

@login_required
def post_reply(request, topic_id):
    form = PostForm()
    topic = Topic.objects.get(pk=topic_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, )))

    return render_to_response('django_simple_forum/reply.html', {
            'form': form,
            'topic': topic,
        }, context_instance=RequestContext(request))

@login_required
def new_topic(request, forum_id):
    form = TopicForm()
    forum = get_object_or_404(Forum, pk=forum_id)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('forum-detail', args=(forum_id, )))

    return render_to_response('django_simple_forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
