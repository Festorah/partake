import pytest
from django.contrib.auth import get_user_model
from events.models import Event

@pytest.fixture
def user_data():
	print('welldone funshy')
	return {'email': 'user_email@gmail.com', 'first_name' : 'user_first_name', 'last_name': 'user_last_name', 'username': 'user_username', 'password': 'user_password1'}


@pytest.fixture
def authenticated_user(client, user_data):
	user_model = get_user_model()
	test_user = user_model.objects.create_user(**user_data)
	test_user.set_password(user_data.get('password'))
	test_user.save()
	client.login(**user_data)
	return test_user

@pytest.fixture
def event_data():
	print('yeah')
	return {'name': 'event_name'}

@pytest.fixture
def create_event(client, event_data):
	event = Event.objects.all()
	test_event = event.create(**event_data)
	test_event.save()
	return test_event
