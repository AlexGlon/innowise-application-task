from django.urls import reverse
from rest_framework import status

from authentication.tests import UserAuthenticationTestCaseCore
from tickets.factories import TicketFactory


def ticket_generation(batch_size):
    """Auxiliary function for generating Faker ticket data."""
    tickets = TicketFactory.create_batch(batch_size)

    ticket_data_list = []
    for ticket in tickets:
        ticket_data = {
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'user': ticket.user.id,
            'creation_time': ticket.creation_time,
        }
        ticket_data_list.append(ticket_data)

    # returning a single dict in case we have generated only 1 ticket
    if ticket_data_list.__len__() == 1:
        return ticket_data_list[0]
    else:
        return ticket_data_list


def ticket_id_extraction(response_data):
    """Auxiliary function for getting ticket ID from the URL sent in response JSON."""
    return response_data['url'].split('/')[-2]


class TicketsTestCase(UserAuthenticationTestCaseCore):

    def test_list_tickets(self):
        """Tests for ticket listing."""
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: separate this into several tests?
    def test_create_ticket(self):
        """Tests for ticket creation."""
        ticket_data = ticket_generation(1)

        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # this block tests the case when user isn't authenticated
        self.client.force_authenticate(user=None)
        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ticket(self):
        """Tests for ticket deletion."""
        ticket_data = ticket_generation(1)
        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ticket_id = ticket_id_extraction(response.data)

        # first we check whether unauthorized user can delete tickets
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'/tickets/{ticket_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: rewrite this?
        # sending a request with authorization credentials to test authenticated user's behaviour
        response = self.client.delete(f'/tickets/{ticket_id}/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_ticket(self):
        """Tests for ticket update procedure."""
        ticket_data = ticket_generation(1)
        response = self.client.post('/tickets/', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ticket_id = ticket_id_extraction(response.data)

        new_ticket_data = ticket_generation(1)

        response = self.client.put(f'/tickets/{ticket_id}/', data=new_ticket_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.put(f'/tickets/{ticket_id}/', data=new_ticket_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_by_user_view(self):
        """Tests for 'List tickets by selected user' view."""
        tickets_data = ticket_generation(15)

        user_id_list = []
        for ticket in tickets_data:
            user_id_list.append(ticket['user'])
            self.client.post('/tickets/', data=ticket)

        for user in user_id_list:
            response = self.client.get(f'/tickets/by_user/{user}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        for user in user_id_list:
            response = self.client.get(f'/tickets/by_user/{user}/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
