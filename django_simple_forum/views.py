from django.template import RequestContext
from django.forms import models as forms_models
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django_simple_forum.models import Category, Forum, Topic, Post
from django_simple_forum.forms import TopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from gamerauntsia.log.models import Log
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
    try:
        user = request.user.id
    except:
        user = None

    topic = Topic.objects.get(pk=topic_id)
    topic.sum_visits(user)
    return render_to_response("django_simple_forum/topic.html", add_csrf(request, forum=forum, posts=posts, pk=topic_id,
        topic=topic), context_instance=RequestContext(request))

@login_required
def close_topic(request, slug, topic_id):
    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(topic=topic_id).order_by("created")

    topic = get_object_or_404(Topic, pk=topic_id)
    topic.closed = True
    topic.save()
    return HttpResponseRedirect(reverse('topic-detail', args=(slug,topic.id)))

@login_required
def post_reply(request, slug, topic_id):

    quote = request.GET.get('quote', '')
    author = request.GET.get('author', '')
    if quote:
        quote = '<blockquote>'+quote+'<footer>'+author+'</footer></blockquote>'

    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(topic=topic_id).order_by("created").reverse()[:3]
    topic = Topic.objects.get(pk=topic_id)

    form_title = ''
    if topic.last_post():
        form_title = 'Re: ' + topic.last_post().title.replace('Re: ','')

    default_data = {'title': form_title,'body':'Zure erantzuna...'}
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

            l = Log()
            l.mota = 'Foroa'
            l.tituloa = 'Erantzun berria'
            l.deskripzioa = topic 
            l.user = request.user
            l.post_id = post.id
            l.forum_id = forum.id
            l.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(slug,topic.id, )))

    return render_to_response('django_simple_forum/reply.html', {
            'form': form,
            'topic': topic,
            'forum': forum,
            'posts': posts,
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
            topic.description = ''
            topic.creator = request.user
            topic.save()
            
            topic.forums.add(forum)
            topic.save()
            
            post = Post()
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['description']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']
            post.topic = topic
            post.save()

            l = Log()
            l.mota = 'Foroa'
            l.tituloa = 'Gai berria'
            l.deskripzioa = post.title
            l.post_id = post.id
            l.user = request.user
            l.forum_id = forum.id
            l.save()


            return HttpResponseRedirect(reverse('topic-detail', args=(slug,topic.id, )))

    return render_to_response('django_simple_forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
