from django.contrib import admin
from django.conf.urls import url
from .models import Course
from .models import Event
from django.core.exceptions import PermissionDenied
from django.contrib.admin.utils import unquote
from django.http import Http404, HttpResponseRedirect
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from .models import User
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    #fields = ('name',)
    #readonly_fields = ('name', 'state')
    search_fields = ['name']
    ordering = ('id',)
    list_display = ('name', 'acciones')

    class Media:
        css = {
            "all": ("custom/css/course_style.css",)
        }

    def get_urls(self):
        return [
            url(
                r'^(.+)/calendario/$',
                self.admin_site.admin_view(self.calendario),
                name='show_curso_calendario',
            ),
        ] + super().get_urls()

    def calendario(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        course = self.get_object(request, unquote(id))
        if course is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            title='Calendario por curso',
            # adminForm=adminForm,
            form_url=form_url,
            # form=form,
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            add=True,
            change=False,
            has_delete_permission=False,
            has_change_permission=True,
            has_absolute_url=False,
            opts=self.model._meta,
            original=course,
            save_as=False,
            show_save=True,
        )
        return TemplateResponse(request, "calendario/index.html", context)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'color')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'get_color')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super().lookup_allowed(lookup, value)
