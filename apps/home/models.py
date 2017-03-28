from django.db import models
from django.utils.html import format_html
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst


class User(AbstractUser):
    color = models.CharField(max_length=16)

    class Meta(AbstractUser.Meta):
        # swappable = 'AUTH_USER_MODEL' #ver django-angular-seed
        verbose_name = capfirst(_('user'))
        verbose_name_plural = capfirst(_('users'))

    def __str__(self):
        return self.username

    def get_color(self):
        return format_html("<span style='background:%s'>%s</span>" % (self.color, self.color))


class Platform(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"

    def __str__(self):
        return self.name

    def acciones(self):
        if self.state:
            return format_html(
                """<a href="%s/calendario" class="link_btn_actions">Ir a calendario</a>
            <a href="%s/descargas" class="link_btn_actions">Ir a Descargas</a>""" % (self.pk, self.pk)
            )
        else:
            return u''


class CourseGroup(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    platform = models.ForeignKey(Platform)

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField('Estado', default=False)
    isDownload = models.BooleanField('¿Esta descargado?', default=False)
    user = models.ForeignKey('User', blank=True, null=True)
    group = models.ForeignKey(CourseGroup)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User)
    platform = models.ForeignKey(Platform)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return u"%s -> %s %s" % (self.user.username, self.start, self.end)

    def color(self):
        return self.user.color

    def title(self):
        if(self.user.first_name):
            return u"%s %s" % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username
