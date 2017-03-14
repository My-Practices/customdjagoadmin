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


class Course(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta(AbstractUser.Meta):
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name

    def acciones(self):
        if self.state:
            return format_html(
                """<a href="%s/calendario" class="link_btn_actions">Ir a calendario</a>
            <a href="#" class="link_btn_actions">Ir a Descargas</a>""" % (self.pk)
            )
        else:
            return u''


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
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
