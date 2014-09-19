from django.template import RequestContext

from django.forms import models as forms_models

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.context_processors import csrf

from django_simple_forum.models import Category, Forum, Topic, Post
from django_simple_forum.forms import TopicForm, PostForm

#from guest.decorators import guest_allowed, login_required
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from settings import *

def index(request):
    """Main listing."""
    categories = Category.objects.all().order_by('order')
    return render_to_response("django_simple_forum/list.html", {'categories': categories, 
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

def forum(request, slug):
    """Listing of topics in a forum."""
    top_topics = Topic.objects.filter(block_top=True,forum__slug=slug).order_by("-created")
    topics = Topic.objects.filter(block_top=False,forum__slug=slug).order_by("-created")
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

    forum = get_object_or_404(Forum, slug=slug)

    return render_to_response("django_simple_forum/forum.html", add_csrf(request, top_topics=top_topics,topics=topics, forum=forum),
                              context_instance=RequestContext(request))

def topic(request, slug, topic_id):
    """Listing of posts in a topic."""
    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(topic=topic_id).order_by("created")
    posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
    topic = Topic.objects.get(pk=topic_id)
    return render_to_response("django_simple_forum/topic.html", add_csrf(request, forum=forum, posts=posts, pk=topic_id,
        topic=topic), context_instance=RequestContext(request))

@login_required
def post_reply(request, slug, topic_id):
    
    quote = request.GET.get('quote', '')
    author = request.GET.get('author', '')
    if quote:
        quote = '<blockquote><p>'+quote+'...</p><footer>'+author+'</footer></blockquote><br/><br/>'
    
    form = PostForm()
    forum = get_object_or_404(Forum, slug=slug)
    topic = Topic.objects.get(pk=topic_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = form.cleaned_data['title']
            post.body = quote + form.cleaned_data['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(slug,topic.id, )))

    return render_to_response('django_simple_forum/reply.html', {
            'form': form,
            'topic': topic,
            'forum': forum,
        }, context_instance=RequestContext(request))

@login_required
def new_topic(request, slug):
    form = TopicForm()
    forum = get_object_or_404(Forum, slug=slug)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('forum-detail', args=(slug, )))

    return render_to_response('django_simple_forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
