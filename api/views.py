import json

from django.http import JsonResponse
from rest_framework.decorators import api_view

from src.estimator import estimator


@api_view(['POST',])
def index(request):
    data = parse_request(request.data)
    return JsonResponse(estimator(data))


def parse_request(request):
    data = dict()
    for key in request.keys():
        if key == 'region':
            data.setdefault(key, json.loads(request.get(key)))
        else:
            data.setdefault(key, request.get(key))
    return data