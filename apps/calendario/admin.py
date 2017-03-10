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
    readonly_fields = ('name', 'state')
    search_fields = ['name']
    list_display = ('name', 'acciones')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    #fields = ('start', 'end')
    #readonly_fields = ('name', 'state')
    list_display = ('user', 'start', 'end')
