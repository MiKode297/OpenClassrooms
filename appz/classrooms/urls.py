from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('signup', views.signup, name='signup'),
    path("signin", views.signin, name="signin"),
    path("api_index", views.api_index, name="api_index"),
    # path('signout', views.signout, name='signout'),
]
