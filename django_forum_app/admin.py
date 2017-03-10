from django.contrib import admin
from django_forum_app.models import Category, Forum, Topic, Post, ProfaneWord
from django_forum_app.forms import PostAdminForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["order", "title"]


class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "category", "creator", "created"]
    prepopulated_fields = {"slug": ("title",)}


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created", "block_top"]
    list_filter = ["creator", ]
    filter_horizontal = ('forums',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "topic", "creator", "created"]
    raw_id_fields = ('creator', 'topic')
    form = PostAdminForm


class ProfaneWordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
