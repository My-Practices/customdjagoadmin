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
        return format_html("""<a href="%s/cal" style="background: #447e9b;padding: 5px 12px;font-weight: 400;font-size: 11px;text-transform: uppercase;letter-spacing: 0.5px;color: #fff;border-radius: 15px;">Ir a calendario</a>""" % (self.pk))


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.user.username
