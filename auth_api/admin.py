from django.contrib import admin

from auth_api.models import User
from django.contrib.auth.admin import UserAdmin
class UserAdminConfig(UserAdmin):
    # model = User
    
    search_fields = ('email','username')
    ordering = ('start_date',)

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # list_filter = ('email','username','is_active','is_staff')
    list_display = ('email','id','username','is_active','is_staff')

    fieldsets = (
        (None,{'fields':('email','username',)}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser')}),
        

    )

    # formfield_overrides = {
    #     User.<if you want to imply on a certain field> : {'widget': Textarea(attrs={'rows':10,'cols':40})},

    # }

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,{
        'classes':('wide',),
        'fields':('email','username','password1','password2','is_staff','is_active'),
        }),

    )

admin.site.register(User, UserAdminConfig)