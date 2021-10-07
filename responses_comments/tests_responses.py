from rest_framework import status

from authentication.tests import UserAuthenticationTestCaseCore
from responses_comments.factories import ResponseFactory

urls = {
    'response_main': '/responses/',
    'response_by_ticket': '/responses/by_ticket/',
    }


def response_generation(batch_size):
    """Auxiliary function for generating Faker response data."""
    responses = ResponseFactory.create_batch(batch_size)

    response_data_list = []
    for response in responses:
        response_data = {
            'initial_ticket': response.initial_ticket.id,
            'content': response.content,
            'support_member': response.support_member.id,
            'time': response.time,
        }
        response_data_list.append(response_data)

    # returning a single dict in case we have generated only 1 response
    if response_data_list.__len__() == 1:
        return response_data_list[0]
    else:
        return response_data_list


def response_id_extraction(response_data):
    """Auxiliary function for getting response ID from the URL sent in response JSON."""
    return response_data['url'].split('/')[-2]


class ResponseTestCase(UserAuthenticationTestCaseCore):
    def test_list_responses(self):
        """Tests response listing."""
        response = self.client.get(f'{urls["response_main"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_response(self):
        """Tests for response creation."""
        response_data = response_generation(1)

        response = self.client.post(f'{urls["response_main"]}', data=response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=None)
        response = self.client.post(f'{urls["response_main"]}', data=response_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_response(self):
        """Tests for response deletion."""
        responses_data = response_generation(1)
        response = self.client.post(f'{urls["response_main"]}', data=responses_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_id = response_id_extraction(response.data)

        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{urls["response_main"]}{response_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: rewrite this?
        response = self.client.delete(f'{urls["response_main"]}{response_id}/',
                                      HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_response(self):
        """Tests for response update procedure."""
        response_data = response_generation(1)
        response = self.client.post(f'{urls["response_main"]}', data=response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_id = response_id_extraction(response.data)

        new_response_data = response_generation(1)

        response = self.client.put(f'{urls["response_main"]}{response_id}/', data=new_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.put(f'{urls["response_main"]}{response_id}/', data=new_response_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_by_ticket_view(self):
        """Tests for 'Load response by ticket ID' view."""
        responses = response_generation(15)

        tickets_id_list = []
        for response in responses:
            tickets_id_list.append(response['initial_ticket'])
            self.client.post(f'{urls["response_main"]}', data=response)

        for ticket in tickets_id_list:
            response = self.client.get(f'{urls["response_by_ticket"]}{ticket}/')
            assert ((response.status_code == status.HTTP_200_OK)
                    or (response.status_code == status.HTTP_204_NO_CONTENT))

        self.client.force_authenticate(user=None)
        for ticket in tickets_id_list:
            response = self.client.get(f'{urls["response_by_ticket"]}{ticket}/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
