import json

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from src.estimator import estimator


@api_view(['POST',])
def index(request):
    data = parse_request(request.data)
    return Response(estimator(data))


@api_view(['POST',])
@renderer_classes((XMLRenderer,))
def xml(request):
    data = parse_request(request.data)
    return Response(estimator(data))


def parse_request(request):
    data = dict()
    for key in request.keys():
        if key == 'region':
            data.setdefault(key, json.loads(request.get(key)))
        else:
            data.setdefault(key, request.get(key))
    return data