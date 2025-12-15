import unittest
from unittest.mock import patch

from datetime import datetime, timedelta

from src.types.node import Node


"""
Unit tests for Node class
"""


class TestNodeParameters(unittest.TestCase):
    """
    Test cases to check the parameters and methods of the Node class
    """

    def test_node_name(self) -> None:
        """
        Test that the name of the node is correctly set
        """

        node: Node = Node(name="home")

        self.assertEqual(node.name, "home")

    def test_node_parent(self) -> None:
        """
        Test that the parent of the node is correctly set
        """

        parent_node: Node = Node(name="parent")
        child_node: Node = Node(name="child", parent=parent_node)

        self.assertEqual(child_node.name, "child")
        self.assertEqual(child_node.parent, parent_node)


class TestNodeDateTimeParameters(unittest.TestCase):
    """
    Test cases to check the created_at and updated_at parameters of the Node class
    """

    def test_created_at(self) -> None:
        """
        Test that the created_at timestamp is set when the node is created
        """

        node = Node(name="test_node")

        self.assertIsInstance(node.created_at, datetime)
        self.assertAlmostEqual(
            node.created_at, datetime.now(), delta=timedelta(seconds=1)
        )

    def test_updated_at(self) -> None:
        """
        Test that the updated_at timestamp is set when the node is updated
        """

        node = Node(name="test_node")
        node.rename("new_name")

        self.assertIsInstance(node.updated_at, datetime)
        self.assertAlmostEqual(
            node.updated_at, datetime.now(), delta=timedelta(seconds=1)
        )

    def test_created_at_and_updated_at(self):
        """
        Test that the created_at and updated_at timestamps are set when the node is created and updated
        """
        with patch("src.types.node.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
            node = Node(name="test_node")

            self.assertIsInstance(node.created_at, datetime)
            self.assertIsInstance(node.updated_at, datetime)
            self.assertEqual(node.created_at, datetime(2023, 1, 1, 12, 0, 0))
            self.assertEqual(node.updated_at, datetime(2023, 1, 1, 12, 0, 0))

            # Simulate an update
            mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 1)
            node.rename("new_name")

            self.assertIsInstance(node.updated_at, datetime)
            self.assertEqual(node.updated_at, datetime(2023, 1, 1, 12, 0, 1))
