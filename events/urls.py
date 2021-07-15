from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('services/', views.services, name='services'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('add_events/', views.add_events, name='add_events'),
	path('register/', views.register, name='register'),
    path('check_in/', views.check_in, name='check_in'),
    path('chatroom/<int:pk>/', views.chat_room, name='chat-room'),
    path('chatroom_message/', views.chat_room_message, name='chat-room-message'),
    path('upvote/<slug:slug>/', views.upvote, name='upvote'),
    path('events_list/', views.events_list, name='events-list'),
    path('search/', views.search, name='search'),
    path('event_detail/<slug:slug>/', views.event_detail, name='event-detail'),
    path('event_sub/<slug:slug>/', views.event_sub, name='event-sub'),
    path('app_sub/', views.app_sub, name='app-sub'),
    path('event_reg/<int:pk>/', views.event_reg, name='event_reg'),
    path('blog_detail/', views.blog_detail, name='blog-detail'),
]
