"""
Implements a light-weight git to commit and push to GitHub.
"""

from gitlit.utils import *
import enum
import os
import sys
from gevent.libev.corecext import self
import hashlib
import path
from zipfile import zlib

class GitLit(enum.Enum):
    commit = 1
    tree = 2
    blob = 3

    def init(repo):
        """Create directory for repo and initialize .git directory."""
        from distutils.file_util import write_file
        if os.path.isdir(repo):
            """
            @todo: raise exception
            """
            if os.path.isdir(os.path.join(repo, '.git')):
                sys.exit(1)
            else:
                os.mkdir(os.path.join(repo, 'git'))
        else:
            os.mkdir(repo)
            os.mkdir(os.path.join(repo, 'git'))
        
        for name in ['objects', 'refs', 'refs/heads']:
            os.mkdir(os.path.join(repo, '.git', name))
        write_file(os.path.join(repo, '.git', 'HEAD'), b'ref: refs/heads/master')
        print('Initialized empty repository: {}'.format(repo))
        
    
    def hash_object(self, data, obj_type, write=True):
        """
        Computes hash of object data of a given type.
        If 'write' is True writes to object store.
        Returns
        -------
        SHA-1 object as a hash string  
        """
        from distutils.file_util import write_file
        header = '{} {}'.format(obj_type, len(data)).encode()
        full_data = header + b'x\00' + data
        sha1 = hashlib.sha1(full_data).hexdigest()
        if write:
            path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok= True)
                write_file(path, zlib.compress(full_data))
        return sha1
    
    def commit(self):
        pass
    
    
    def status(self):
        pass
    
    
    def diff(self):
        pass
    
    
    def add(self):
        pass
    
    
    def checkout(self):
        pass
    
    
    def branch(self):
        pass
    
    
    def lof(self):
        pass
    
    
    def merge(self):
        pass
    
    
    def push(self):
        pass            
                
        