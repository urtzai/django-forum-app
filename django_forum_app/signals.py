from django.template import loader, Context
from django.core.mail import send_mail
from django.db.models import Count
from django.conf import settings
from django.contrib.sites.models import Site
from .models import Post

FORUM_SUBJECT = getattr(settings, 'FORUM_SUBJECT', "FORUM")


def send_post_email(sender, instance, **kwargs):
    if kwargs['created']:
        t = loader.get_template('post_email.txt')
        c = Context({ 'domain': Site.objects.get_current().domain, 'url': instance.get_absolute_url(), 'forums': instance.topic.forums.all()})
        message = t.render(c)

        creators = Post.objects.filter(topic=instance.topic).values('creator__email').annotate(n=Count("creator__id"))
        for creator in creators:
            if not instance.creator.email == creator['creator__email']:
                send_mail('[' + FORUM_SUBJECT + ' - ' + instance.topic.title + ']', message, settings.DEFAULT_FROM_EMAIL, [creator['creator__email']])


def send_topic_email(sender, instance, **kwargs):
    if kwargs['created']:
        t = loader.get_template('topic_email.txt')
        c = Context({ 'domain': Site.objects.get_current().domain, 'id': instance.id})
        message = t.render(c)
        
        for forum in instance.forums.all():
            creator = forum.creator
            creator.email_user(subject='[' + FORUM_SUBJECT + ' - ' + instance.title + ']', message=message, from_email=settings.DEFAULT_FROM_EMAIL)