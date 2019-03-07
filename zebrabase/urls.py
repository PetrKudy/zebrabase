"""zebrabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from management.views import Index, RoomView,SelectRackView,RackView,FishDetailView,AddRoomView,UpdateRoomView,DeleteRoomView,AddRackView,UpdateRackView,DeleteRackView,AddFishDetailView,UpdateFishDetailView,DeleteFishDetailView
from django.urls import include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_required(Index.as_view()),name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    ## rooms
    path('rooms/',login_required(RoomView.as_view()),name='rooms'),
    path('rooms/add',login_required(AddRoomView.as_view()),name='room_add'),
    path('rooms/<int:pk>/update',login_required(UpdateRoomView.as_view()),name='room_update'),
    path('rooms/<int:pk>/delete',login_required(DeleteRoomView.as_view()),name='room_delete'),
    ## racks
    path('rooms/<int:pk>',login_required(SelectRackView.as_view()),name = 'SelectRack'),
    path('rooms/<int:room_pk>/rack/<int:pk>',login_required(RackView.as_view()), name = 'rack'),
    path('rooms/<int:pk>/rack/add',login_required(AddRackView.as_view()),name='rack_add'),
    path('rooms/<int:room_pk>/rack/<int:pk>/update',login_required(UpdateRackView.as_view()),name='rack_update'),
    path('rooms/<int:room_pk>/rack/<int:pk>/delete',login_required(DeleteRackView.as_view()),name='delete_view'),
    ## fishs
    path('fishdetail/<int:pk>',login_required(FishDetailView.as_view()), name = 'fishdetail'),
    path('fishdetail/<int:rack>/create/<int:row>/<int:col>',login_required(AddFishDetailView.as_view()), name = 'fish_add'),
    path('fishdetail/<int:pk>/update',login_required(UpdateFishDetailView.as_view()), name = 'fish_update'),
    path('fishdetail/<int:pk>/delete',login_required(DeleteFishDetailView.as_view()), name = 'fish_delete'),

]
