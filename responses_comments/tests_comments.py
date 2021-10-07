from rest_framework import status

from authentication.tests import UserAuthenticationTestCaseCore
from responses_comments.factories import CommentFactory

urls = {
    'comment_main': '/comments/',
    'response_main': '/responses/',
    'response_thread': '/comments/',
}


def comment_generation(batch_size):
    """Auxiliary function for generating Faker comment data."""
    comments = CommentFactory.create_batch(batch_size)

    comment_data_list = []
    for comment in comments:
        comment_data = {
            'initial_response': comment.initial_response.id,
            'initial_comment': comment.initial_comment,
            'content': comment.content,
            'user': comment.user.id,
            'time': comment.time,
        }
        comment_data_list.append(comment_data)

    # returning a single dict in case we have generated only 1 response
    if comment_data_list.__len__() == 1:
        return comment_data_list[0]
    else:
        return comment_data_list


def comment_id_extraction(response_data):
    """Auxiliary function for getting comment ID from the URL sent in response JSON."""
    return response_data['url'].split('/')[-2]


class CommentTestCase(UserAuthenticationTestCaseCore):
    def test_list_comments(self):
        """Tests comment listing."""
        response = self.client.get(f'{urls["comment_main"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        """Tests for comment creation."""
        comment_data = comment_generation(1)

        response = self.client.post(f'{urls["comment_main"]}', data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=None)
        response = self.client.post(f'{urls["comment_main"]}', data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment(self):
        """Tests for comment deletion."""
        comment_data = comment_generation(1)
        response = self.client.post(f'{urls["comment_main"]}', data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment_id = comment_id_extraction(response.data)

        self.client.force_authenticate(user=None)
        response = self.client.delete(f'{urls["comment_main"]}{comment_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: rewrite this?
        response = self.client.delete(f'{urls["comment_main"]}{comment_id}/', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_comment(self):
        """Tests for comment update procedure."""
        comment_data = comment_generation(1)
        response = self.client.post(f'{urls["comment_main"]}', data=comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment_id = comment_id_extraction(response.data)

        new_comment_data = comment_generation(1)

        response = self.client.put(f'{urls["comment_main"]}{comment_id}/', data=new_comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.put(f'{urls["comment_main"]}{comment_id}/', data=new_comment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: move to `tests_responses` since this endpoint belongs to comments model views?
    def test_comments_thread_view(self):
        """Tests for 'List all comments to a support response' view."""
        comments_data = comment_generation(15)

        source_responses = []
        for comment in comments_data:
            source_responses.append(comment['initial_response'])
            self.client.post(f'{urls["comment_main"]}', data=comment)

        for support_response in source_responses:
            response = self.client.get(f'{urls["response_main"]}{support_response}{urls["response_thread"]}')
            assert ((response.status_code == status.HTTP_200_OK)
                    or (response.status_code == status.HTTP_204_NO_CONTENT))

        self.client.force_authenticate(user=None)
        for support_response in source_responses:
            response = self.client.get(f'{urls["response_main"]}{support_response}{urls["response_thread"]}')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
