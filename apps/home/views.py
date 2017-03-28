from django.core import serializers
from django.http import HttpResponse
from .models import Event
from django.conf import settings
from django.shortcuts import redirect
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.shortcuts import get_object_or_404


def GetEventsAjax(request):
        # error
        # metodo si no hay id
        # si no vimno id
        #
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.is_ajax():
        if request.method == 'GET' and 'id' in request.GET.keys():
            # =======================Listar eventos========================
            eventos = Event.objects.filter(platform_id=request.GET.get('id'))
            eventos_json = []
            for e in eventos:
                eventos_json.append({
                    "id": e.id,
                    "start": e.start,
                    "end": e.end,
                    "color": e.color(),
                    "editable": request.user == e.user,
                    "startEditable": False,
                    "overlap": False,
                    "title": e.title(),
                    "isOwner": request.user == e.user
                })
            u = datetime.datetime.now()
            d = datetime.timedelta(weeks=2)
            eventos_json.append({
                "start": u - d,
                "end": u,
                "overlap": False,
                "rendering": 'background',
                "color": '#ff9f89'
            })
            data = json.dumps(eventos_json, cls=DjangoJSONEncoder)
        elif request.method == 'POST' and 'platform' in request.POST.keys():
                # =======================Agregar evento========================
            e = Event()
            e.start = request.POST.get('start')
            e.end = request.POST.get('end')
            e.user = request.user
            e.platform_id = request.POST.get('platform')
            e.save()
            data = json.dumps(e.id, cls=DjangoJSONEncoder)
        elif request.method == 'POST' and 'id' in request.POST.keys():
                # =======================Eliminar evento=======================
            e = get_object_or_404(Event, pk=request.POST.get('id'))
            if e.user == request.user:
                e.delete()
                data = json.dumps("OK",
                                  cls=DjangoJSONEncoder)
            else:
                data = 'No tienes permiso para eliminar.'
        elif request.method == 'POST' and 'pk' in request.POST.keys():
                # =======================Modificar evento=====================
            e = get_object_or_404(Event, pk=request.POST.get('pk'))
            if e.user == request.user:
                e.start = request.POST.get('start')
                e.end = request.POST.get('end')
                e.save()
                data = json.dumps(e.pk, cls=DjangoJSONEncoder)
            else:
                data = json.dumps(
                    "No tienes permiso para modificar", cls=DjangoJSONEncoder)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')
