from django.template import RequestContext

from django.forms import models as forms_models

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404

from django.core.urlresolvers import reverse
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

def forum(request, slug):
    """Listing of topics in a forum."""
    top_topics = Topic.objects.filter(block_top=True,forums__slug=slug).order_by("-created")
    topics = Topic.objects.filter(block_top=False,forums__slug=slug).order_by("-created")
    
    topics = list(top_topics) + list(topics)

    forum = get_object_or_404(Forum, slug=slug)

    return render_to_response("django_simple_forum/forum.html", add_csrf(request, topics=topics, forum=forum),
                              context_instance=RequestContext(request))

def topic(request, slug, topic_id):
    """Listing of posts in a topic."""
    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(topic=topic_id).order_by("created")
    
    topic = Topic.objects.get(pk=topic_id)
    return render_to_response("django_simple_forum/topic.html", add_csrf(request, forum=forum, posts=posts, pk=topic_id,
        topic=topic), context_instance=RequestContext(request))

@login_required
def post_reply(request, slug, topic_id):
    
    quote = request.GET.get('quote', '')
    author = request.GET.get('author', '')
    if quote:
        quote = '<blockquote>'+quote+'<footer>'+author+'</footer></blockquote>'
    
    forum = get_object_or_404(Forum, slug=slug)
    topic = Topic.objects.get(pk=topic_id)
    
    form_title = ''
    if topic.last_post():
        form_title = 'Re: ' + topic.last_post().title.replace('Re: ','')
    
    default_data = {'title': form_title,'body':''}
    form = PostForm(default_data)
    
    if request.method == 'POST':
        quote = request.POST.get('quote', '')
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
            'quote': quote,
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
            topic.creator = request.user

            topic.save()
            topic.forums.add(forum)
            topic.save()

            return HttpResponseRedirect(reverse('forum-detail', args=(slug, )))

    return render_to_response('django_simple_forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
