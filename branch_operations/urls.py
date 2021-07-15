from django.urls import path
from . import views

urlpatterns = [
	path('first_timers/', views.first_timers, name='first-timers'),
	path('service_attendance/', views.service_attendance, name='service-attendance'),
	path('converts/', views.converts, name='converts'),
	path('branch_dashboard/', views.branch_dashboard, name='branch-dashboard'),
	path('new_converts_db/', views.new_converts_db, name='new-converts-db'),
	path('first_timers_db/', views.first_timers_db, name='first-timers-db'),
	path('service_detail/<int:pk>/', views.service_detail, name='service-detail'),
]


