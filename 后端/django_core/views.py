from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def status(request):
    return Response({"detail": "Survey Platform Backend is running! Please refer to https://app.swaggerhub.com/apis/cp13/CP13/1.0.0 for the API documentation."})