from src.root import FileSystem
from src.utils import exceptions

from src.root.config import logger


class FileSystemCLI:
    def __init__(self):
        self.fs = FileSystem()
        self.commands = {
            "mkdir": self.make_directory,
            "touch": self.make_file,
            "cd": self.change_directory,
            "ls": self.list_contents,
            "rm": self.delete_node,
            "mv": self.move_node,
            "cp": self.copy_node,
            "cat": self.read_file,
            "echo": self.write_file,
            "pwd": self.print_working_directory,
            "find": self.find_node,
            "grep": self.grep_files,
            "tree": self.show_tree,
            "help": self.show_help,
            "exit": self.exit_cli,
        }

    def make_directory(self, args):
        if args:
            dir_name = args[0]
            self.fs.mkdir(dir_name)
        else:
            logger.error("Usage: mkdir <directory_name>")

    def make_file(self, args):
        if args:
            file_name = args[0]
            self.fs.touch(file_name)
        else:
            logger.error("Usage: touch <file_name>")

    def change_directory(self, args):
        if args:
            dir_name = args[0]
            self.fs.cd(dir_name)
            logger.info(f"Changed directory to '{dir_name}'.")
        else:
            logger.error("Usage: cd <directory_name>")

    def list_contents(self, args):
        contents = self.fs.ls()
        
        # Check if -l flag is provided for detailed listing
        if args and args[0] == "-l":
            from src.types import File, Directory
            for node in contents:
                node_type = "d" if isinstance(node, Directory) else "f"
                size = f"{node.size}B" if isinstance(node, File) else "-"
                created = node.created_at.strftime("%Y-%m-%d %H:%M")
                logger.info(f"{node_type}  {size:>8}  {created}  {node.name}")
        else:
            for node in contents:
                logger.info(node.name)

    def delete_node(self, args):
        if args:
            node_name = args[0]
            try:
                self.fs.rm(node_name)
                logger.info(f"Node '{node_name}' deleted.")
            except FileNotFoundError as e:
                logger.error(e)
        else:
            logger.error("Usage: rm <node_name>")

    def move_node(self, args):
        if len(args) == 2:
            src_name, dest_name = args
            try:
                self.fs.mv(src_name, dest_name)
                logger.info(f"Moved '{src_name}' to '{dest_name}'.")
            except FileNotFoundError as e:
                logger.error(e)
        else:
            logger.error("Usage: mv <source> <destination>")

    def copy_node(self, args):
        if len(args) == 2:
            src_name, dest_name = args
            try:
                self.fs.cp(src_name, dest_name)
                logger.info(f"Copied '{src_name}' to '{dest_name}'.")
            except FileNotFoundError as e:
                logger.error(e)
        else:
            logger.error("Usage: cp <source> <destination>")

    def read_file(self, args):
        if args:
            file_name = args[0]
            try:
                content = self.fs.cat(file_name)
                logger.info(content if content else "(empty file)")
            except FileNotFoundError as e:
                logger.error(e)
        else:
            logger.error("Usage: cat <file_name>")

    def write_file(self, args):
        if len(args) >= 3:
            # Find the position of ">" to split content and filename
            if ">" in args:
                redirect_idx = args.index(">")
                if redirect_idx > 0 and redirect_idx < len(args) - 1:
                    content = " ".join(args[:redirect_idx])
                    file_name = args[redirect_idx + 1]
                    try:
                        # Find the file and write to it
                        for child in self.fs.current.children:
                            if child.name == file_name:
                                child.write_content(content)
                                logger.info(f"Content written to '{file_name}'.")
                                return
                        logger.error(f"File '{file_name}' not found.")
                    except Exception as e:
                        logger.error(e)
                else:
                    logger.error("Usage: echo <text> > <file_name>")
            else:
                logger.error("Usage: echo <text> > <file_name>")
        else:
            logger.error("Usage: echo <text> > <file_name>")

    def print_working_directory(self, args):
        current_path = self.fs.get_current_path()
        logger.info(current_path)

    def find_node(self, args):
        if args:
            name = args[0]
            results = self.fs.find(name)
            if results:
                logger.info(f"Found {len(results)} match(es):")
                for node in results:
                    logger.info(f"  {node.get_path()}")
            else:
                logger.info(f"No matches found for '{name}'.")
        else:
            logger.error("Usage: find <name>")

    def grep_files(self, args):
        if args:
            pattern = " ".join(args)
            results = self.fs.grep(pattern)
            if results:
                logger.info(f"Found {len(results)} match(es):")
                for file_path, line_num, line in results:
                    logger.info(f"{file_path}:{line_num}: {line}")
            else:
                logger.info(f"No matches found for pattern '{pattern}'.")
        else:
            logger.error("Usage: grep <pattern>")

    def show_tree(self, args):
        def print_tree(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            logger.info(prefix + connector + node.name)
            
            if hasattr(node, 'children') and node.children:
                extension = "    " if is_last else "│   "
                for i, child in enumerate(node.children):
                    is_last_child = i == len(node.children) - 1
                    print_tree(child, prefix + extension, is_last_child)
        
        logger.info(self.fs.current.name)
        if hasattr(self.fs.current, 'children'):
            for i, child in enumerate(self.fs.current.children):
                is_last = i == len(self.fs.current.children) - 1
                print_tree(child, "", is_last)

    def show_help(self, args):
        logger.info("Available commands:")
        for command in self.commands:
            logger.info(command)

    def exit_cli(self, args):
        logger.info("Exiting CLI.")
        exit()

    def run(self):
        logger.info("Welcome to the FileSystem CLI. v1.0.0\n")
        while True:
            current_path = self.fs.get_current_path()
            command_input = input(f"{current_path} $ ").strip().split()
            if not command_input:
                continue
            command = command_input[0]
            args = command_input[1:]
            if command in self.commands:
                self.commands[command](args)
            else:
                try:
                    raise exceptions.UnknownCommandError(
                        f"Unknown command: {command}. Type 'help' for a list of commands."
                    )
                except exceptions.UnknownCommandError as e:
                    logger.error(e)


if __name__ == "__main__":
    FileSystemCLI().run()
