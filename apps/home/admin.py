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
from .forms import CourseForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    #fields = ('name',)
    #readonly_fields = ('name', 'state')
    search_fields = ['name']
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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    #fields = ('start', 'end')
    #readonly_fields = ('name', 'state')
    list_display = ('user', 'start', 'end')
