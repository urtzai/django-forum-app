from django import forms
from django_forum_app.models import Topic, Post, ProfaneWord
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _
from django.conf import settings

TINYMCE_BODY_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {})
DJANGO_FORUM_APP_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_FORUM_APP_FILTER_PROFANE_WORDS', False)


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(
        attrs={'cols': 80, 'rows': 30, 'placeholder': _("Your answer...")}, mce_attrs=TINYMCE_BODY_CONFIG))

    class Meta:
        model = Post
        fields = ('body',)


class TopicForm(forms.ModelForm):

    title = forms.CharField(label=_("Title"), max_length=60, required=True)
    description = forms.CharField(label=_("First message"), widget=TinyMCE(
        attrs={'cols': 80, 'rows': 30, 'placeholder': _("Write your answer here!")}, mce_attrs=TINYMCE_BODY_CONFIG))

    class Meta():
        model = Topic
        fields = ('title', 'description')


class PostForm(forms.ModelForm):
    body = forms.CharField(label=_('Body'), widget=TinyMCE(
        attrs={'cols': 80, 'rows': 30, 'class': 'my_tinymce', 'placeholder': _("Your answer...")},
        mce_attrs=TINYMCE_BODY_CONFIG,
    ))

    class Meta():
        model = Post
        exclude = ('creator', 'updated', 'created', 'topic', 'user_ip', 'telegram_id')

    def clean_body(self):
        body = self.cleaned_data["body"]

        if DJANGO_FORUM_APP_FILTER_PROFANE_WORDS:
            profane_words = ProfaneWord.objects.all()
            bad_words = [w for w in profane_words if w.word in body.lower()]

            if bad_words:
                raise forms.ValidationError(_("Bad words like '%s' are not allowed in posts.") % (reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))

        return body
