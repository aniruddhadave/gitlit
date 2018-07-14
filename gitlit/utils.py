"""
Utilities

@author: Aniruddha Dave
"""
import zlib

def read_file(path):
    """Reads contents of file as bytes."""
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    """Writes data bytes to file at given path."""
    with open(path, 'wb') as f:
        f.write(data)
        
def find_object(sha1_prefix):
    """
    Finds object with the given SHA-1 prefix.
    Returns the path to object in object store
    Raises a ValueError if there are no objects or multiple objects
    """
    if (len(sha1_prefix) < 2):
        raise ValueError("Hash prefix must have 2 or more characters")
    
    obj_dir = os.path.join('.git', 'objects', sha1_prefix[:2])
    rmng = sha1_prefix[2:]
    objects = [name for name in os.listdir(obj_dir) if name.startswith(rmng)]
    if not objects:
        raise ValueError("Object {} not found".format(sha1_prefix))
    if len(objects) >= 2:
        raise ValueError("Multiple objects ({}) with prefix {}".format(
            len(objects), sha1_prefix))
    return os.path.join(obj_dir, objects[0])

def read_object(sha1_prefix):
    """
    Reads object with given SHA-1 prefix
    Return a tuple(object_type , data_bytes)
    Raises ValueError of object not found
    """
    from builtins import int
    path = find_object(sha1_prefix)
    data_full = zlib.decompress(read_file(path))
    idx = data_full.index(b'\x00')
    header = data_full[:idx] 
    object_type, size_data = header.decode().split()
    size = int(size_data)
    data = data_full[idx + 1:]
    size_recvd = len(data)
    assert size == len(data), 'expected size {} but received {} bytes'.format(
        size, size_recvd)
    return (object_type, data)
        