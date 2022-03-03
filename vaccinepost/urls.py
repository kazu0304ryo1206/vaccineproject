from django.contrib import admin
from django.urls import path
from .views import loginview,placeview,calendarview,timeview,confirmview,last_monthview,next_monthview,decisionview,decision2view,selectview,decision3view,decision4view,login2view,select2view,decision5view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',loginview,name='login'),
    path('place/',placeview,name='place'),
    path('calendar/',calendarview,name='calendar'),
    path('time/',timeview,name='time'),
    path('confirm/',confirmview,name='confirm'),
    path('last_month/',last_monthview,name='last_month'),
    path('next_month/',next_monthview,name='next_month'),
    path('decision/<int:i>',decisionview,name='decision'),
    path('decision2/<str:time>',decision2view,name='decision2'),
    path('decision3/<str:i>/',decision3view,name='decision3'),
    path('decision4/',decision4view,name='decision4'),
    path('decision5/<str:i>/',decision5view,name='decision5'),
    path('select/',selectview,name='select'),
    path('login2/',login2view,name='login2'),
    path('select2/',select2view,name='select2'),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
