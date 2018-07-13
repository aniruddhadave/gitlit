"""
Utilities

@author: Aniruddha Dave
"""

def read_file(path):
    """Reads contents of file as bytes."""
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    """Writes data bytes to file at given path."""
    with open(path, 'wb') as f:
        f.write(data)