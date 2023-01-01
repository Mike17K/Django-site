from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("home",views.index,name="index"),
    path("aboutUs",views.aboutUs,name="aboutUs"),
    path("contactUs",views.contactUs,name="contactUs"),
    path("gallery",views.gallery,name="gallery"),
    path("createCanvas",views.createCanvas,name="createCanvas"),
    path("createTable",views.createTable,name="createTable"),
]