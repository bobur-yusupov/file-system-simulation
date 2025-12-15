from typing import Optional, List, Union
from datetime import datetime

from .node import Node
from src.utils.exceptions import FileNotFoundError


class Directory(Node):
    """
    Directory class inherits from Node
    class and represents a directory in the file system.
    """

    def __init__(
        self,
        name: str,
        parent: Optional[Node] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(name, parent, created_at)

        parent.add_child(self) if parent else None

        self.children: List[Node] = []

    def __repr__(self) -> str:
        return f"Directory(name={self.name}, parent={self.parent}, \
                created_at={self.created_at}, updated_at={self.updated_at})"

    def get_path(self) -> str:
        return super().get_path()

    def rename(self, new_name: str) -> None:
        super().rename(new_name)

    def add_child(self, new_child: "Node") -> None:
        """
        Add a child node to the current node
        """

        self.children.append(new_child)
        new_child.parent = self

    def remove_child(self, child: Union[Node, str]) -> None:
        """
        Remove a child node from the current node
        
        :param child: Either a Node object or a string name of the child to remove
        """
        if isinstance(child, str):
            # Find the child by name
            for node in self.children:
                if node.name == child:
                    self.children.remove(node)
                    node.parent = None
                    return
            raise FileNotFoundError(f"Node '{child}' not found")
        else:
            # Remove by Node object
            self.children.remove(child)
            child.parent = None

    def list_children(self) -> List["Node"]:
        """
        List the children of the current node
        """
        return self.children
