from typing import List, Optional

from src.types import Node, Directory, File
from src.root.config import logger


class FileSystem:
    def __init__(self):
        self.root = Directory("/root", None)

        # Create some default directories
        self.home = Directory("home", parent=self.root)
        self.bin = Directory("bin", parent=self.root)
        self.media = Directory("media", parent=self.root)

        self.current = self.root

    def ls(self) -> List[Node]:
        return self.current.list_children()

    def cd(self, directory_name):
        if directory_name == "..":
            if self.current.parent is not None:
                self.current = self.current.parent
        else:
            for child in self.current.children:
                if child.name == directory_name and isinstance(child, Directory):
                    self.current = child
                    return
            raise FileNotFoundError(f"Directory '{directory_name}' not found")

    def mkdir(self, name) -> Optional[Directory]:
        for child in self.current.children:
            if child.name == name and isinstance(child, Directory):
                logger.error(f"Directory '{name}' already exists.")
                return None

        new_directory = Directory(name=name, parent=self.current)
        self.current.add_child(new_directory)
        logger.warning(f"Directory '{name}' created.")

        return new_directory

    def touch(self, name: str) -> Optional[File]:
        for child in self.current.children:
            if child.name == name and isinstance(child, File):
                logger.error(f"File '{name}' already exists.")
                return None
        new_file = File(name=name, parent=self.current)
        self.current.add_child(new_file)
        logger.info(f"File '{name}' created.")
        return new_file

    def cat(self, name: str) -> str:
        """
        Reading the content of a file.
        """
        for child in self.current.children:
            if child.name == name and isinstance(child, File):
                return child.read_content()
        raise FileNotFoundError(f"File '{name}' not found")

    def rm(self, name: str) -> None:
        self.current.remove_child(name)

    def rmdir(self, name) -> None:
        for child in self.current.children:
            if child.name == name and isinstance(child, Directory):
                self.current.remove_child(name)
                return
        raise FileNotFoundError(f"Directory '{name}' not found")

    def mv(self, src_name: str, dest_name: str) -> None:
        """
        Move or rename a file or directory.
        """
        # Find the source node
        src_node = None
        for child in self.current.children:
            if child.name == src_name:
                src_node = child
                break
        
        if src_node is None:
            raise FileNotFoundError(f"'{src_name}' not found")
        
        # Check if destination is a directory that exists
        dest_node = None
        for child in self.current.children:
            if child.name == dest_name and isinstance(child, Directory):
                dest_node = child
                break
        
        if dest_node:
            # Move into the destination directory
            self.current.remove_child(src_node)
            dest_node.add_child(src_node)
        else:
            # Rename the source node
            src_node.rename(dest_name)

    def cp(self, src_name: str, dest_name: str) -> None:
        """
        Copy a file or directory.
        """
        # Find the source node
        src_node = None
        for child in self.current.children:
            if child.name == src_name:
                src_node = child
                break
        
        if src_node is None:
            raise FileNotFoundError(f"'{src_name}' not found")
        
        # Check if destination is a directory that exists
        dest_node = None
        for child in self.current.children:
            if child.name == dest_name and isinstance(child, Directory):
                dest_node = child
                break
        
        if isinstance(src_node, File):
            # Copy file
            if dest_node:
                # Copy into directory
                new_file = File(name=src_node.name, parent=dest_node)
                new_file.write_content(src_node.read_content())
                dest_node.add_child(new_file)
            else:
                # Copy with new name in current directory
                new_file = File(name=dest_name, parent=self.current)
                new_file.write_content(src_node.read_content())
                self.current.add_child(new_file)
        else:
            # Copy directory (shallow copy)
            if dest_node:
                new_dir = Directory(name=src_node.name, parent=dest_node)
                dest_node.add_child(new_dir)
            else:
                new_dir = Directory(name=dest_name, parent=self.current)
                self.current.add_child(new_dir)

    def find(self, name: str) -> List[Node]:
        """
        Find all nodes with the given name in the current directory and subdirectories.
        """
        results = []
        
        def search(node: Directory):
            for child in node.children:
                if child.name == name:
                    results.append(child)
                if isinstance(child, Directory):
                    search(child)
        
        search(self.current)
        return results

    def get_current_path(self) -> str:
        return self.current.get_path()

    def __str__(self):
        return str(self.current)
