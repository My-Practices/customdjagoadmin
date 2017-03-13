from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name

    def acciones(self):
        return format_html(
            """<a href="%s/calendario" class="link_btn_actions">Ir a calendario</a>
            <a href="#" class="link_btn_actions">Ir a Descargas</a>""" % (self.pk)
        )


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
        return u'red'

    def title(self):
        if(self.user.first_name):
            return u"%s %s" % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username
