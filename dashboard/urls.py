from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard, name='dashboard-home'),
	path('events_db/', views.events_db, name='events-db'),
	path('check_in_db/<int:pk>', views.check_in_db, name='checkin-db'),
	path('registered_attendees/<int:pk>', views.registered_attendees, name='registered_attendees'),
	path('attendance_db/', views.attendance_db, name='attendance-db'),
	path('checkin_details/<int:pk>', views.checkin_details, name='checkin-details'),
	path('checkin_details_pdf/<int:pk>', views.render_pdf_view, name='render-pdf-view'),
]


