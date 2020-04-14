from django.http import JsonResponse
from rest_framework.decorators import api_view

from src.estimator import estimator


@api_view(['POST',])
def index(request):
    return JsonResponse(estimator(request.data))