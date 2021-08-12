from django.urls import path, re_path

from . import views

app_name = 'Chat'


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('open-new-chat/<slug:tlt>/', views.new_chat_view, name='NewChat'),
#    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
