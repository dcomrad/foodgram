from django.contrib import admin

from .models import Followers, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'followers_amount')
    search_fields = ('username', 'email')

    def followers_amount(self, obj):
        return Followers.objects.filter(author=obj).count()

    followers_amount.short_description = 'Число подписчиков'


class FollowersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_filter = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Followers, FollowersAdmin)
