import json
import os

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


@api_view(['GET',])
def logs(request):
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = []
    with open(os.path.join(DIR, 'requests.txt'), 'r') as reader:
        for line in reader.readlines():
            data.append(line.replace('\n', ''))
    return Response(data, content_type='text/plain; charset=UTF-8')


def parse_request(request):
    data = dict()
    for key in request.keys():
        if key == 'region':
            data.setdefault(key, json.loads(request.get(key)))
        else:
            data.setdefault(key, request.get(key))
    return data