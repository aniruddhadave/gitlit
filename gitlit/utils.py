"""
Utilities

@author: Aniruddha Dave
"""
import zlib
import sys
from sphinx.util.pycompat import sys_encoding
from bkcharts.stats import stats

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

def cat_file(mode, sha1_prefix):
    """
    Writes the contents or the info about the object with given SHA-1 prefix to stdout.
    Prints raw data bytes if mode is 'commit', 'tree' or 'blob'
    Prints size of the object if mode is 'size'
    Prints type of the object if mode is 'type'
    Prints pretty version of the object if mode is 'pretty'
    """
    object_type , data = read_object(sha1_prefix)
    if mode in ['commit', 'tree', 'blob']:
        if object_type != mode:
            raise ValueError('Expected object type {} but received {}'.
                             format(mode, object_type))
        sys.stdout.write(data)
    elif mode == 'type':
        print (object_type)
    elif mode == 'size':
        print(len(data))
    elif mode == 'pretty':
        if object_type in ['commit', 'blob']:
            sys_encoding.stdout.write(data)
        elif object_type == 'tree':
            for mode, path, sha1 in read_tree(data=data):
                type_string = 'tree' if stat.S_ISDIR(mode) else 'blob'
        else:
            assert False, 'Unhandled object type: {}'.format(object_type)
    else:
        raise ValueError('Unexpected mode type: {}'.format(mode))
        