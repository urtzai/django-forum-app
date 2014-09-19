from django.conf import settings

DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE = getattr(settings, 'DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE', 10)
DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE = getattr(settings, 'DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE', 10)
DJANGO_SIMPLE_FORUM_FILTER_PROFANE_WORDS = getattr(settings, 'DJANGO_SIMPLE_FORUM_FILTER_PROFANE_WORDS', True)
TINYMCE_BODY_CONFIG = {
    #mode : "textareas",
    "mode" : "exact",
    "elements" : "body",
    "convert_urls" : False,    
    "extended_valid_elements" : "iframe[src|name|width|height|align|frameborder|marginwidth|marginheight|scrolling]",
    "theme" : "advanced",
    "theme_advanced_buttons1" : "styleselect,bold,italic,underline,separator,bullist,numlist,blockquote,undo,redo,link,unlink,image,code,removeformat,cut,copy,paste,pastetext,pasteword,selectall,pastetext,",
    "theme_advanced_buttons2" : "",
    "theme_advanced_buttons3" : "",
    "theme_advanced_toolbar_location" : "top",
    "theme_advanced_toolbar_align" : "left",
    "plugins" : "paste",
    "paste_auto_cleanup_on_paste" : True,
    "paste_use_dialog" : False,
    "forced_root_block" : "",  
    "force_br_newlines" : True,
    "force_p_newlines" : False,
    "content_css" : "/static/css/stylehtmleditor.css",
    "extended_valid_elements" : "object[width|height|classid|codebase],param[name|value],embed[src|type|width|height|flashvars|wmode]",
}
