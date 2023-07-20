from allauth.account.utils import send_email_confirmation
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def update_user(request):
    first_name = request.data["first_name"] if "first_name" in request.data else None
    last_name = request.data["last_name"] if "last_name" in request.data else None
    user = request.user
    if first_name is None or first_name == "":
        pass
    else:
        user.first_name = first_name
    if last_name is None or last_name == "":
        pass
    else:
        user.last_name = last_name
    user.save()
    return Response({"detail": "Name updated."})


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def send_verification_email(request):
    send_email_confirmation(request, request.user)
    return Response({"detail": "Verification email sent"})


@api_view(["GET"])
@permission_classes([IsAuthenticated, ])
def delete_user(request):
    user = request.user
    try:
        user.delete()
    # catch-all exception
    # if not logged in, the authentication wrapper should return 403 instead
    except Exception:
        return Response({"detail": "User cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
    # return success if deletion successful
    return Response({"detail": "User has been deleted"})