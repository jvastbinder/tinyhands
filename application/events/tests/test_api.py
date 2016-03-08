import datetime
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.tests.factories import ViewUserFactory
from events.tests.factories import EventFactory

class RestApiTestCase(APITestCase):

    def login(self, user):
        self.client = APIClient()
        self.client.force_authenticate(user=user)

class CalendarFeedAPITests(RestApiTestCase):

    def test_when_not_logged_in_should_return_403_error(self):
        url = reverse('EventCalendarFeed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_when_no_start_and_end_date_in_query_should_return_400_error(self):
        url = reverse('EventCalendarFeed')
        user = ViewUserFactory.create()
        self.login(user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Date does not match format %Y-%m-%d')

    def test_when_start_date_is_later_than_end_date_should_return_400_error(self):
        url = reverse('EventCalendarFeed')
        user = ViewUserFactory.create()
        start_date = datetime.date.today()
        end_date = start_date - datetime.timedelta(days=7)
        self.login(user)

        response = self.client.get(url, {'start': start_date, 'end': end_date})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Start date is later than end date')

    def test_when_dates_are_valid_should_return_events_in_date_range(self):
        url = reverse('EventCalendarFeed')
        user = ViewUserFactory.create()
        event = EventFactory.create()
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=2)
        outsideEvent = EventFactory.create(start_date=end_date+datetime.timedelta(days=1), end_date=end_date+datetime.timedelta(days=2))
        self.login(user)

        response = self.client.get(url, {'start': start_date, 'end': end_date})

        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['title'], event.title)
        self.assertEquals(response.data[0]['location'], event.location)

    def test_when_event_is_repeated_should_return_multiple_events(self):
        url = reverse('EventCalendarFeed')
        user = ViewUserFactory.create()
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=2)
        repeatedEventProperties = {
            'start_date': start_date,
            'end_date': end_date,
            'is_repeat': True,
            'repetition': 'D',
            'ends': end_date + datetime.timedelta(days=4)
        }
        repeatedEvent = EventFactory.create(**repeatedEventProperties)
        self.login(user)

        response = self.client.get(url, {'start': start_date, 'end': end_date})

        self.assertEquals(len(response.data), 2)
        self.assertEquals(response.data[0]['title'], repeatedEvent.title)
        self.assertEquals(response.data[0]['location'], repeatedEvent.location)
        self.assertEquals(response.data[1]['title'], repeatedEvent.title)
        self.assertEquals(response.data[1]['location'], repeatedEvent.location)


