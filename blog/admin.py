from django.contrib import admin
from .models import Post


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ register post model in admin panel """
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # for display filed in main admin page
    list_filter = ["status", "created", "publish", "author"]  # right side create list filter for filter item by this
    search_fields = ["title", "body"]  # for search filed search in this filed
    prepopulated_fields = {"slug": ("title",)}  # for automatic write in the slug filed by the title filed enters
    raw_id_fields = ['author']  # for display a foreignKey in admin panel in new style instead of dropdown select input
    date_hierarchy = 'publish'  # for show data history created
    ordering = ['status', 'publish']  # ordering this is just in admin panel
