import json
from django.test import TestCase
try:
    from django.core.urlresolvers import reverse
except ImportError:  # django < 1.10
    from django.urls import reverse
from django.test import Client
from django_forum_app.models import Category, Forum, Topic, Post
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
from django.core.mail import outbox


class BasicTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cat = Category.objects.create(order=1, title="General")
        forum = Forum.objects.create(title="The Beatles", slug="the-beatles", category=cat, creator=user)
        topic = Topic.objects.create(title="Which is the first album's name?", creator=user)
        topic.forums.add(forum)
        topic.save()
        Post.objects.create(title="My opinion", creator=user, topic=topic, body="I think is Please Please Me")

    def test_forum_index_view(self):
        c = Client()
        url = reverse('forum-index')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_forum_detail_view(self):
        c = Client()
        url = reverse('forum-detail', kwargs={'slug': "the-beatles"})
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_detail_view(self):
        c = Client()
        url = reverse('topic-detail', kwargs={'slug': "the-beatles", 'topic_id': 1})
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view(self):
        c = Client()
        c.login(username='john', password='johnpassword')
        url = reverse('new-topic', kwargs={'slug': "the-beatles"})
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_post(self):
        c = Client()
        c.login(username='john', password='johnpassword')
        url = reverse('new-topic', kwargs={'slug': "the-beatles"})
        response = c.post(url, {'title': "I don't like The Beatles", 'description': "It's the worst band of the history!"})
        topic_url = reverse('topic-detail', kwargs={'slug': "the-beatles", 'topic_id': 2})
        self.assertRedirects(response, topic_url)
        #self.assertEqual(len(outbox), 1)

    def test_close_topic_post(self):
        c = Client()
        c.login(username='john', password='johnpassword')
        url = reverse('close-topic', kwargs={'slug': "the-beatles", "topic_id": 1})
        response = c.get(url)
        topic_url = reverse('topic-detail', kwargs={'slug': "the-beatles", 'topic_id': 1})
        self.assertRedirects(response, topic_url)

    def test_post_reply(self):
        c = Client()
        c.login(username='john', password='johnpassword')
        url = reverse('reply', kwargs={'slug': "the-beatles", "topic_id": 1})
        response = c.post(url, {'title': "I think you are wrong", 'body': "Not sure, but that's not the first album!"})
        topic_url = reverse('topic-detail', kwargs={'slug': "the-beatles", 'topic_id': 1})
        self.assertRedirects(response, topic_url)
        #self.assertEqual(len(outbox), 1)
