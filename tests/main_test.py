import unittest
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app
from src.models import User, Task
from src.auth import get_current_user, RoleChecker
from unittest.mock import patch

client = TestClient(app)

mock_admin_user = User(username="admin", role="admin")
mock_readonly_user = User(username="readonly", role="readonly")

mock_task = Task(
    id=1,
    name="Test Task",
    status="pending",
    created_at=datetime.now(),
    updated_at=datetime.now()
)

mock_tasks = [mock_task]

# Mock roles


def override_admin_user():
    return mock_admin_user


def override_readonly_user():
    return mock_readonly_user


def always_true_dependency():
    return True


class TaskAPITestCase(unittest.TestCase):

    def setUp(self):
        # Apply dependency overrides before each test
        app.dependency_overrides[get_current_user] = override_admin_user
        app.dependency_overrides[RoleChecker("admin")] = always_true_dependency
        app.dependency_overrides[RoleChecker("readonly")] = always_true_dependency

    def tearDown(self):
        # Clear overrides after each test
        app.dependency_overrides = {}

    @patch("src.queries.get_all_tasks", return_value=mock_tasks)
    def test_list_tasks_as_admin(self, _):
        """
        Test case for listing tasks as an admin user.

        This test verifies that an admin user can successfully retrieve the list of tasks
        via a GET request to the "/tasks" endpoint. It checks that the response status code
        is 200 (OK) and validates the name of the first task in the response.

        Assertions:
            - The response status code is 200.
            - The name of the first task in the response JSON is "Test Task".
        """
        response = client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Test Task")

    @patch("src.queries.get_task_by_id", return_value=mock_task)
    def test_get_task_by_id(self, _):
        """
        Test case for retrieving a task by its ID.

        This test verifies that the API endpoint for retrieving a task by its ID
        returns the correct HTTP status code (200) and that the response contains
        the expected task ID.

        Steps:
        1. Send a GET request to the endpoint "/tasks/1".
        2. Assert that the response status code is 200.
        3. Assert that the "id" field in the JSON response is 1.

        Args:
            _: Mocked dependency or unused parameter (if applicable).
        """
        response = client.get("/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    @patch("src.queries.create_task", return_value=mock_task)
    def test_create_task_as_admin(self, _):
        """
        Test case for creating a task as an admin user.

        This test verifies that an admin user can successfully create a new task
        by sending a POST request to the "/tasks" endpoint with the required data.

        Assertions:
            - The response status code should be 200, indicating success.
            - The "name" field in the response JSON should match the expected value.
        """
        response = client.post("/tasks", json={"name": "New Task"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Task")

    @patch("src.queries.update_task", return_value=mock_task)
    def test_update_task_as_admin(self, _):
        """
        Test case for updating a task as an admin user.

        This test simulates an admin user sending a PUT request to update
        a task with new data. It verifies that the response status code
        is 200 (indicating success) and checks that the returned task
        status is as expected (mocked as "pending" in this case).

        Assertions:
            - The response status code is 200.
            - The "status" field in the response JSON is "pending".
        """
        response = client.put("/tasks/1", json={"name": "Updated Task", "status": "completed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "pending")

    @patch("src.queries.delete_task", return_value=mock_task)
    def test_delete_task_as_admin(self, _):
        """
        Test case for deleting a task as an admin user.

        This test verifies that an admin user can successfully delete a task
        by sending a DELETE request to the endpoint `/tasks/1`. It checks that
        the response status code is 200 (indicating success) and that the
        response JSON contains the correct task ID.

        Args:
            self: The test case instance.
            _: Placeholder for any unused arguments.

        Assertions:
            - The response status code is 200.
            - The response JSON contains the correct task ID (1).
        """
        response = client.delete("/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)


if __name__ == '__main__':
    unittest.main()
