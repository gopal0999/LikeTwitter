from django.contrib import admin

# Register your models here.
from .models import Tweet,TweetLike

class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['id','content', 'user__username', 'user__email']
    class Meta:
        model = Tweet

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

# class TweetLikeAdmin(admin.ModelAdmin):
#     list_display = ['tweet','user']
#     search_fields = ['tweet__id','tweet__content', 'user__username', 'user__email']
#     class Meta:
#         model = TweetLike


admin.site.register(Tweet, TweetAdmin)
# admin.site.register(TweetLike, TweetLikeAdmin)
