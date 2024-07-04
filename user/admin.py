from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Code


class UserCreationform(forms.ModelForm):
    """ Form for creating new users. Includes all the required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_user_name',
            'last_user_name',
            'gender',
            'nationality',
            'province',
            'district',
            'city',
            'profession',
            'provenance'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ Form for updating users. Includes all the fields on the user,
    but replaces the password field with admin's password hash display field
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationform

    list_display = (
            'email',
            'first_user_name',
            'last_user_name',
            'gender',
            'nationality',
            'province',
            'district',
            'city',
            'profession',
            'provenance',
            'birthday',
            'contact'
        )

    list_filter = ('admin', 'staff', 'active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': (
            'first_user_name',
            'last_user_name',
            'gender',
            'nationality',
            'province',
            'district',
            'city',
            'profession',
            'provenance',
            'birthday',
            'contact'
        )
        }),
        ('Permissions', {'fields': ('active', 'staff', 'admin', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide', ),
                'fields': ('email', 'first_user_name', 'last_user_name', 'gender', 'nationality', 'province', 'district', 'city', 'profession', 'provenance', 'birthday', 'contact', 'password1', 'password2')})
    )

    search_fields = ('email', 'first_user_name', 'last_user_name')
    ordering = ('email',)
    filter_horizontal = ('groups',)


admin.site.register(User, UserAdmin)
admin.site.register(Code)
