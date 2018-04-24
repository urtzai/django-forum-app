from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .signals import send_post_email, send_topic_email


class DjangoForumAppConfig(AppConfig):
   name = 'django_forum_app'
   verbose_name = _('Forum')

   def ready(self):
       topic = self.get_model('Topic')
       post = self.get_model('Post')
       post_save.connect(send_topic_email, sender=Topic)
       post_save.connect(send_post_email, sender=Post)