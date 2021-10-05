from django.urls import reverse
from rest_framework import status

from authentication.tests import UserAuthenticationTestCaseCore
from tickets.factories import TicketFactory


class TicketsTestCase(UserAuthenticationTestCaseCore):
    @staticmethod
    def ticket_generation():
        """Auxiliary function for generating Faker ticket data."""
        ticket = TicketFactory()
        ticket_data = {
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'user': ticket.user.id,
            'creation_time': ticket.creation_time,
        }
        return ticket_data

    def test_list_tickets(self):
        """Tests for ticket listing."""
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: separate this into several tests?
    def test_create_ticket(self):
        """Tests for ticket creation."""
        ticket_data = self.ticket_generation()

        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # this block tests the case when user isn't authenticated
        self.client.force_authenticate(user=None)
        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tickets(self):
        """Tests for ticket deletion."""
        ticket_data = self.ticket_generation()
        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # getting ticket ID from URL sent in response JSON
        ticket_id = response.data['url'].split('/')[-2]

        # first we check whether unauthorized user can delete tickets
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'/tickets/{ticket_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: rewrite this?
        # sending a request with authorization credentials to test authenticated user's behaviour
        response = self.client.delete(f'/tickets/{ticket_id}/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
