from django import urls
from django.contrib.auth import get_user_model
from events.models import Event
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('param', [
	('home'),
	('services'),
	('contact'),
	('register'),
	('check_in'),
	('add_events'),
	('about'),
	('events-list'),
	('search'),
])
def test_render_views_events(client, param):
	temp_url = urls.reverse(param)
	resp = client.get(temp_url)
	assert resp.status_code == 200


@pytest.mark.django_db
def test_reg_event(client, authenticated_user, create_event, event_data):
	event = Event.objects.get(pk=create_event.pk)
	event_reg_url = urls.reverse('event_reg' , create_event.pk)
	resp = client.get(event_reg_url, data=create_event.pk)
	assert resp.status_code == 200



