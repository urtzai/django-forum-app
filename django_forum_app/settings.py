from django.conf import settings

FORUM_SUBJECT = getattr(settings, 'FORUM_SUBJECT', "FORUM")

POSTS_PER_PAGE = getattr(settings, 'POSTS_PER_PAGE', 10)

DJANGO_FORUM_APP_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_FORUM_APP_FILTER_PROFANE_WORDS', True)

TINYMCE_DEFAULT_CONFIG = {
    "language": 'en',
    "theme": "modern",
    "height": 600,
    "plugins": [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste",
    ],
    "toolbar": "styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview",
    "menubar": False,
    "media_alt_source": False,
    "media_poster": False,
    "media_dimensions": False,
}
