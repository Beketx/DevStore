from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password', 'name', 'surname',
						   'last_login', 'phone', 'role', 'iin',
						   'gender', 'is_joined', 'city')}),
			  ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
									'groups', 'user_permissions',
									)
						}
			  ),
		)
	add_fields = (
		(
			None,
			{
				'classes': ('wide',),
				'fields': ('email', )
			}
			),
		)
	# exclude = ('username', )
	list_display = ('email', 'name', 'surname', 'last_login', 'phone','gender')
	list_filter = ('is_superuser', 'is_active', 'groups')
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)
admin.site.register(City)
# admin.site.register(PhoneOTP)