import unittest
from src.root import FileSystem
from src.types import File, Directory


class TestFileSystemOperations(unittest.TestCase):
    """
    Tests for FileSystem operations
    """
    
    def setUp(self):
        """Set up a fresh filesystem for each test"""
        self.fs = FileSystem()
    
    def _file_exists(self, name):
        """Helper method to check if a file/directory exists in current directory"""
        for child in self.fs.current.children:
            if child.name == name:
                return True
        return False
    
    def test_mv_rename_file(self):
        """Test renaming a file using mv"""
        self.fs.touch("oldname.txt")
        self.fs.mv("oldname.txt", "newname.txt")
        
        # Check that oldname doesn't exist
        self.assertFalse(self._file_exists("oldname.txt"))
        
        # Check that newname exists
        self.assertTrue(self._file_exists("newname.txt"))
    
    def test_mv_move_file_to_directory(self):
        """Test moving a file into a directory"""
        self.fs.touch("file.txt")
        self.fs.mkdir("subdir")
        self.fs.mv("file.txt", "subdir")
        
        # File should not be in current directory
        self.assertFalse(self._file_exists("file.txt"))
        
        # File should be in subdir
        subdir = None
        for child in self.fs.current.children:
            if child.name == "subdir":
                subdir = child
                break
        
        self.assertIsNotNone(subdir)
        found = False
        for child in subdir.children:
            if child.name == "file.txt":
                found = True
        self.assertTrue(found)
    
    def test_cp_copy_file(self):
        """Test copying a file"""
        file1 = self.fs.touch("original.txt")
        if file1:
            file1.write_content("Hello, World!")
        
        self.fs.cp("original.txt", "copy.txt")
        
        # Both files should exist
        self.assertTrue(self._file_exists("original.txt"))
        self.assertTrue(self._file_exists("copy.txt"))
        
        # Content should be the same
        content = self.fs.cat("copy.txt")
        self.assertEqual(content, "Hello, World!")
    
    def test_find(self):
        """Test finding nodes"""
        self.fs.touch("test.txt")
        self.fs.mkdir("subdir")
        self.fs.cd("subdir")
        self.fs.touch("test.txt")
        self.fs.cd("..")
        
        results = self.fs.find("test.txt")
        # Should find at least 2 test.txt files
        self.assertGreaterEqual(len(results), 2)
    
    def test_cat_read_file(self):
        """Test reading file content"""
        file1 = self.fs.touch("readme.txt")
        if file1:
            file1.write_content("This is a test file")
        
        content = self.fs.cat("readme.txt")
        self.assertEqual(content, "This is a test file")
    
    def test_cat_nonexistent_file(self):
        """Test reading a non-existent file raises error"""
        with self.assertRaises(FileNotFoundError):
            self.fs.cat("nonexistent.txt")


if __name__ == "__main__":
    unittest.main()
