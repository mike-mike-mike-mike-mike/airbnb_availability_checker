from django.contrib import admin

from .models import User, UserSetting

admin.site.register(User)
admin.site.register(UserSetting)
