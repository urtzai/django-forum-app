from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django_forum_app.signals import send_post_email, send_topic_email


class DjangoForumAppConfig(AppConfig):
   name = 'django_forum_app'
   verbose_name = _('Forum')

   def ready(self):
       Topic = self.get_model('Topic')
       Post = self.get_model('Post')
       post_save.connect(send_topic_email, sender=Topic)
       post_save.connect(send_post_email, sender=Post)