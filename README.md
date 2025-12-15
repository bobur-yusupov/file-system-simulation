# File System simulation

## Overview

This project is a simulation of a file system implemented in Python. It allows users to create, delete, and manage files and directories in a virtual environment.

## Features

- Create and delete files and directories
- Navigate through directories
- List contents of directories (with detailed view option)
- Read and write file contents
- Move and copy files and directories
- Search for files by name
- Search file contents with pattern matching
- Display directory tree structure
- Full path navigation and tracking

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/file-system-simulation.git
```

2. Navigate to the project directory:

```bash
cd file-system-simulation
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start the simulation:

```bash
python run.py
```

## Available Commands

### File and Directory Management
- `mkdir <directory>` - Create a new directory
- `touch <file>` - Create a new file
- `rm <file/directory>` - Remove a file or directory
- `mv <source> <destination>` - Move or rename a file/directory
- `cp <source> <destination>` - Copy a file or directory

### Navigation and Viewing
- `cd <directory>` - Change to a directory (use `..` to go up)
- `pwd` - Print current working directory path
- `ls` - List contents of current directory
- `ls -l` - List contents with detailed information (type, size, date)
- `tree` - Display directory structure as a tree

### File Content Operations
- `cat <file>` - Display file contents
- `echo <text> > <file>` - Write text to a file

### Search Operations
- `find <name>` - Find files/directories by name
- `grep <pattern>` - Search for pattern in file contents

### Utility
- `help` - Show all available commands
- `exit` - Exit the file system simulation

## Examples

### Basic Operations

```bash
# Create a directory
/root $ mkdir documents

# Navigate to it
/root $ cd documents

# Create a file
/root/documents $ touch readme.txt

# Write content to the file
/root/documents $ echo Hello World > readme.txt

# Read the file content
/root/documents $ cat readme.txt
Hello World

# List files with details
/root/documents $ ls -l
f      49B  2024-01-15 10:30  readme.txt
```

### Advanced Operations

```bash
# Copy a file
/root/documents $ cp readme.txt backup.txt

# Move a file to another directory
/root/documents $ mkdir archive
/root/documents $ mv backup.txt archive

# Display directory tree
/root/documents $ tree
documents
├── readme.txt
└── archive
    └── backup.txt

# Find files by name
/root $ find readme.txt
Found 1 match(es):
  /root/documents/readme.txt

# Search file contents
/root $ grep "Hello"
Found 1 match(es):
/root/documents/readme.txt:1: Hello World

# Show current path
/root/documents $ pwd
/root/documents
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
