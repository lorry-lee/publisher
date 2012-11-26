
from django.conf import settings

from publisher.apps.post.models import *
from django.contrib import admin

# TODO: Remove this after refactor
class PostAdmin(admin.ModelAdmin):
    exclude = ('category', )
    list_display = ('title', 'is_public', )
    list_filter = ('is_public', )

admin.site.register(PostType)
admin.site.register(ProductType)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(Profile)
admin.site.register(LevelInfo)
admin.site.register(Publisher)
