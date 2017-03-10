from django.conf import settings

POSTS_PER_PAGE = 10

DJANGO_FORUM_APP_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_FORUM_APP_FILTER_PROFANE_WORDS', True)

TINYMCE_DEFAULT_CONFIG = {
    "language": 'eu',
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
    "content_css": "/static/css/tinymce_content.css",
    "valid_elements": "@[class],p[align],h1,h2,h3,h4,h5,h6,a[href|target],strong/b,div[align],br,table,tbody,thead,tr,td,ul,ol,li,img[src|alt],em",
    "extended_valid_elements": "iframe[src|name|width|height|align|frameborder|marginwidth|marginheight|scrolling],object[width|height|classid|codebase|name|id],param[name|value],embed[src|type|width|height|flashvars|wmode|bgcolor|quality|allowscriptaccess|allowfullscreen]",
}
