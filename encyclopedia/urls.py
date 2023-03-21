from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/",views.create,name="create"),
    path("wiki/",views.random1,name="random1"),
    path("wiki/<str:name>",views.search1,name="search1"),
    path("wiki/edit/<str:toedit>",views.edit,name="edit"),
]
