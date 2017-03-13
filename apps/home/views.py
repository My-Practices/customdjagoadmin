from django.core import serializers
from django.http import HttpResponse
from .models import Event
from django.conf import settings
from django.shortcuts import redirect
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime


def GetEventsAjax(request):
        # error
        # metodo si no hay id
        # si no vimno id
        #
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.is_ajax():
        if request.method == 'GET':
            eventos = Event.objects.filter(course_id=request.GET.get('id'))
            # data = serializers.serialize("json", eventos)
            eventos_json = []
            for e in eventos:
                eventos_json.append({
                    "id": e.id,
                    "start": e.start,
                    "end": e.end,
                    "color": e.color(),
                    "editable": False,
                    "startEditable": False,
                    "overlap": False,
                    "title": e.title(),
                    "isOwner": request.user == e.user
                    # aqui comprobare si es mi usuario para que pueda editar
                    #"resourceEditable": False,
                })
            u = datetime.datetime.now()
            d = datetime.timedelta(weeks=2)
            print(u)
            eventos_json.append({
                "start": u - d,
                "end": u,
                "overlap": False,
                "rendering": 'background',
                "color": '#ff9f89'
            })
            data = json.dumps(eventos_json, cls=DjangoJSONEncoder)
        elif request.method == 'POST':
            e = Event()
            e.start = request.POST.get('start')
            e.end = request.POST.get('end')
            e.user = request.user
            e.course_id = request.POST.get('course')
            e.save()
            """print("##################################")
            print(e)
            # capturar error si no se guarda
            evento = Event.objects.filter(
                course_id=request.POST.get('course')).order_by('-id')
            evento_json = {
                "id": evento[0].id,
                "start": evento[0].start,
                "end": evento[0].end,
                "color": evento[0].color(),
                "editable": False,
                "startEditable": False,
                "overlap": False,
                "title": evento[0].title(),
            }
            data = json.dumps(evento_json, cls=DjangoJSONEncoder)
            """

    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')

"""
def PostDepartamentoAjax(request):
    if request.method == 'POST' and request.is_ajax():
        d = Departamento()
        d.descripcion = request.POST.get('des')
        d.save()

        obj = Departamento.objects.last()
        departamento_json = {}
        departamento_json['pk'] = obj.id
        departamento_json['name'] = obj.descripcion
        data_json = json.dumps(departamento_json)

    else:
        data_json = '{"data":"fail"}'
    return HttpResponse(data_json, content_type='application/json')
    """
