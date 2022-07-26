import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse


from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from appz.classrooms.serializers import UserSerializer, GroupSerializer


@permission_classes([IsAuthenticated])
def api_index(request):
    print(f"WWOOOOOOOOOOOOOOOOOOHHHHAAAAAAAAAAAA: {request}")
    return HttpResponseRedirect(reverse("api_index"))


# @authentication_classes([SessionAuthentication, BasicAuthentication])
@login_required
@permission_classes([IsAuthenticated])
def index(request):
    print(f"WWOOOOOOOOOOOOOOOOOO: {request}")
    return HttpResponse("Hello, world. You're at the OCR index.")


def signin(request):

    response = HttpResponseBadRequest()
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:

        token = Token.objects.create(user=user)
        content = {
            "username": username,
            "email": email,
            "token": token.key,
        }
        response = JsonResponse(content)

    return response


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
