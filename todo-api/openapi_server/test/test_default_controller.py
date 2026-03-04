import unittest

from flask import json

from openapi_server.models.task import Task  # noqa: E501
from openapi_server.models.task_input import TaskInput  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_task(self):
        """Test case for create_task

        Creates a new task.
        """
        task_input = {"completed":False,"title":"Learn OpenAPI"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/tasks',
            method='POST',
            headers=headers,
            data=json.dumps(task_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_task_by_id(self):
        """Test case for get_task_by_id

        Retrieves a task by its ID.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tasks/{task_id}'.format(task_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tasks(self):
        """Test case for get_tasks

        Returns the list of all tasks.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tasks',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
