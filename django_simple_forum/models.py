from django.db import models
from gamerauntsia.gamer.models import GamerUser as User
from photologue.models import Photo
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    order = models.IntegerField()
    title = models.CharField(max_length=60)
    
    def get_forums(self):
        return Forum.objects.filter(category=self.id)
    
    def __unicode__(self):
        return self.title

class Forum(models.Model):
    title = models.CharField(max_length=60)
    slug = slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.ForeignKey(Photo,null=True,blank=True)
    category = models.ForeignKey(Category)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.title
        
    def get_summary(self):
    	if len(self.description) > 100:
    	    return self.description[:100]+'...'
        return self.description

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])

    def last_post(self):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last

class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    forum = models.ForeignKey(Forum)
    block_top = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("-created")[0]

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic)
    body = models.TextField(max_length=10000)
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.topic, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%Y-%m-%d %H:%M"))
        
    def supershort(self):
        return u"%s: %s" % (self.creator, self.created.strftime("%Y-%m-%d %H:%M"))

    short.allow_tags = True


class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word
