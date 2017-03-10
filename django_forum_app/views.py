from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django_forum_app.models import Category, Forum, Topic, Post
from django_forum_app.forms import TopicForm, PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    """Main listing."""
    categories = Category.objects.all().order_by('order')
    return render(request, "django_forum_app/list.html", {'categories': categories, 'user': request.user})


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def forum(request, slug):
    """Listing of topics in a forum."""
    top_topics = Topic.objects.filter(block_top=True, forums__slug=slug).order_by("-created")
    topics = Topic.objects.filter(block_top=False, forums__slug=slug).order_by("-created")

    topics = list(top_topics) + list(topics)

    forum = get_object_or_404(Forum, slug=slug)

    return render(request, "django_forum_app/forum.html", add_csrf(request, topics=topics, forum=forum))


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
    return render(request, "django_forum_app/topic.html", add_csrf(request, forum=forum, posts=posts, pk=topic_id, topic=topic))


@login_required
def close_topic(request, slug, topic_id):
    get_object_or_404(Forum, slug=slug)
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.closed = True
    topic.save()
    return HttpResponseRedirect(reverse('topic-detail', args=(slug, topic.id)))


@login_required
def post_reply(request, slug, topic_id):

    quote = request.GET.get('quote', '')
    author = request.GET.get('author', '')
    if quote:
        quote = '<blockquote>' + quote + '<footer>' + author + '</footer></blockquote>'

    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(topic=topic_id).order_by("created").reverse()[:3]
    topic = Topic.objects.get(pk=topic_id)

    form_title = ''
    if topic.last_post():
        form_title = 'Re: ' + topic.last_post().title.replace('Re: ', '')

    default_data = {'title': form_title, 'body': 'Zure erantzuna...'}
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
            return HttpResponseRedirect(reverse('topic-detail', args=(slug, topic.id, )))

    return render(request, 'django_forum_app/reply.html', {'form': form, 'topic': topic, 'forum': forum, 'posts': posts, 'quote': quote})


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
            return HttpResponseRedirect(reverse('topic-detail', args=(slug, topic.id, )))

    return render(request, 'django_forum_app/new-topic.html', {'form': form, 'forum': forum})
