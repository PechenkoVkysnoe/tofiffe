from django.contrib import admin
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
	list_display = ["id", "username", "first_name", "last_name", "telegram_id", "confirmed"]
	list_editable = ["confirmed"]
	list_filter = ["confirmed"]


admin.site.register(User, UserAdmin)

# Register your models here.
