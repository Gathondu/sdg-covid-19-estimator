import json
import os

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from src.estimator import estimator


@api_view(['POST',])
def index(request):
    data = json.loads(request.body)
    return Response(estimator(data))


@api_view(['POST',])
@renderer_classes((XMLRenderer,))
def xml(request):
    data = json.loads(request.body)
    return Response(estimator(data))


@api_view(['GET',])
def logs(request):
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = []
    with open(os.path.join(DIR, 'requests.txt'), 'r') as reader:
        for line in reader.readlines():
            data.append(line.replace('\n', ''))
    resp = Response(data, content_type='text/plain; charset=UTF-8')
    resp['Content-Disposition'] = ('attachment; filename=res.txt')
    return resp

