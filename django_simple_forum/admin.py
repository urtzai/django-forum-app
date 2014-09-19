from django.contrib import admin
from django_simple_forum.models import Category, Forum, Topic, Post, ProfaneWord

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["order", "title"]

class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "creator", "created"]
    prepopulated_fields = {"slug": ("title",)}

class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "topic", "creator", "created"]

class ProfaneWordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
