"""AuthenticationApp Admin

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser, Engineer, Student, Professor
from .forms import AdminUserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = AdminUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_student', 'is_professor', 'is_engineer')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','programmingLanguage','speciality','yearsOfExperience')}),
        #('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_student', 'is_professor', 'is_engineer')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            #'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    #ordering = ('email','first_name')
    ordering = ('email','first_name', 'is_student', 'is_professor', 'is_engineer')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(Engineer)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.unregister(Group)
