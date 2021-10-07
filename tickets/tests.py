import random

from rest_framework import status

from authentication.tests import UserAuthenticationTestCaseCore
from responses_comments.tests_responses import response_generation
from tickets.factories import TicketFactory


statuses = ['Open', 'Closed', 'Frozen']

urls = {
    'response_main': '/responses/',
    'ticket_by_user': '/tickets/by_user/',
    'ticket_by_status': '/tickets/by_status/',
    'ticket_by_support_member': '/tickets/by_support_member/',
    'ticket_main': '/tickets/',
    'ticket_status_update': '/tickets/status_update/',
    }


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

    def ticket_mass_posting(self, tickets_data):
        """Auxiliary function for posting batches of tickets."""
        for ticket in tickets_data:
            self.client.post(f'{urls["ticket_main"]}', data=ticket)

    def test_list_tickets(self):
        """Tests ticket listing."""
        response = self.client.get(f'{urls["ticket_main"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket(self):
        """Tests for ticket creation."""
        ticket_data = ticket_generation(1)

        response = self.client.post(f'{urls["ticket_main"]}', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # this block tests the case when user isn't authenticated
        self.client.force_authenticate(user=None)
        response = self.client.post(f'{urls["ticket_main"]}', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ticket(self):
        """Tests for ticket deletion."""
        ticket_data = ticket_generation(1)
        response = self.client.post(f'{urls["ticket_main"]}', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ticket_id = ticket_id_extraction(response.data)

        # first we check whether unauthorized user can delete tickets
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{urls["ticket_main"]}{ticket_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: rewrite this?
        # sending a request with authorization credentials to test authenticated user's behaviour
        response = self.client.delete(f'{urls["ticket_main"]}{ticket_id}/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_ticket(self):
        """Tests for ticket update procedure."""
        ticket_data = ticket_generation(1)
        response = self.client.post(f'{urls["ticket_main"]}', data=ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ticket_id = ticket_id_extraction(response.data)

        new_ticket_data = ticket_generation(1)

        response = self.client.put(f'{urls["ticket_main"]}{ticket_id}/', data=new_ticket_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.put(f'{urls["ticket_main"]}{ticket_id}/', data=new_ticket_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_by_user_view(self):
        """Tests for 'List tickets by selected user' view."""
        tickets_data = ticket_generation(15)

        user_id_list = []
        for ticket in tickets_data:
            user_id_list.append(ticket['user'])
            self.client.post(f'{urls["ticket_main"]}', data=ticket)

        for user in user_id_list:
            response = self.client.get(f'{urls["ticket_by_user"]}{user}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        for user in user_id_list:
            response = self.client.get(f'{urls["ticket_by_user"]}{user}/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_by_status_view(self):
        """Tests for 'List tickets by status' view."""
        tickets_data = ticket_generation(15)
        self.ticket_mass_posting(tickets_data)

        for ticket_status in statuses:
            response = self.client.get(f'{urls["ticket_by_status"]}{ticket_status}/')
            # multiple conditions listed so that this test won't fail
            # if, let's say, 'Frozen' status tickets won't generate at all
            assert((response.status_code == status.HTTP_200_OK)
                   or (response.status_code == status.HTTP_204_NO_CONTENT))

        self.client.force_authenticate(user=None)
        for ticket_status in statuses:
            response = self.client.get(f'{urls["ticket_by_status"]}{ticket_status}/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_by_support_member_view(self):
        """Tests for 'List tickets responded by a support member' view."""
        responses_data = response_generation(15)

        support_id_list = []
        for response in responses_data:
            support_id_list.append(response['support_member'])
            self.client.post(f'{urls["response_main"]}', data=response)

        for member in support_id_list:
            response = self.client.get(f'{urls["ticket_by_support_member"]}{member}/')
            assert((response.status_code == status.HTTP_200_OK)
                   or (response.status_code == status.HTTP_204_NO_CONTENT))

        self.client.force_authenticate(user=None)
        for member in support_id_list:
            response = self.client.get(f'{urls["ticket_by_support_member"]}{member}/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ticket_status_update_view(self):
        """Test for 'Update ticket status' view."""
        tickets_data = ticket_generation(15)
        self.ticket_mass_posting(tickets_data)

        # extracting tickets data from the overall tickets list
        posted_tickets_data = self.client.get(f'{urls["ticket_main"]}').data['results']
        ticket_id_list = []
        # extracting IDs of existing tickets
        for ticket in posted_tickets_data:
            ticket_id_list.append(ticket_id_extraction(ticket))

        for ticket in ticket_id_list:
            response = self.client.patch(f'{urls["ticket_status_update"]}{ticket}/',
                                         data={
                                           'status': f'{random.choice(statuses)}'
                                         })
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        for ticket in ticket_id_list:
            response = self.client.patch(f'{urls["ticket_status_update"]}{ticket}/',
                                         data={
                                             'status': f'{random.choice(statuses)}'
                                         })
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
